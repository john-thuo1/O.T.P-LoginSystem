from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from users.models import Client, OTP
from django.contrib import messages
from users.forms import OTPForm, ClientUpdateForm
from django.shortcuts import reverse
from users.send_message import send
from users.generate_code import get_code
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'users/index.html')

def about(request):
    # check if a user has been logged in
    if request.user.is_authenticated:
        return render(request, 'users/about.html')

    return redirect('login')

# the view to be displayed after a user successfully registers
def account_created(request):
    return render(request, 'users/account_created.html')


# The view used to register new users
class ClientCreateView(CreateView):
    # the model the view will use
    model = Client
    fields = ['first_name', 'last_name', 'username', 'phone_number']

    template_name = 'users/profile.html'

    # override this method to get the context data that will 
    # be pushed to the template that will render the view
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # create a new variable inside the context and assign a value to it
        context['form_title'] = 'Sign Up here'
        # return the context
        return context
    
    # override this method that is used to validate the POST data
    def form_valid(self, form):
        # saving the form returns the new user created
        user = form.save()
        # set a default password for the new user created
        user.set_password('123456')
        # save the changes made
        user.save()
        return super(ClientCreateView, self).form_valid(form)

    # override this method that will return the url a user is to be 
    # redirected to once they successfully register/sign up
    def get_success_url(self):
        return reverse('account_created')

# the view to be used when updating user profile
def update_profile(request):    
    # check if the user has been logged in
    if request.user.is_authenticated:
        # if it's a POST request
        if request.method == 'POST':
            # create a form with the client POST data submited and 
            # the instance of the client who's data is to be updated

            # the reason we are passing the client instance is because the 
            # form has been set to associate with the Client model which 
            # has a one to one relationship with the User table
            form = ClientUpdateForm(request.POST,instance=request.user.client)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your profile has been updated')
                return redirect('client-update')
        else:
            # if the request is a GET create a client form with data from the specified client instance
            form = ClientUpdateForm(instance=request.user.client)

        return render(request, 'users/profile.html', {'form': form, 'form_title': 'Update Profile'})
    
    # if user has not logged in
    return redirect('login')

# The view used to display the OTP form page
# When a user logs in they are redirected to this view via a GET request 
def otp(request):
    # if the request is a POST
    # called once a user submits their OTP code
    if request.method == 'POST':
        # generate an OTP form with the POST data
        form = OTPForm(request.POST)
        if form.is_valid():

            # get the OTP code entered
            otp_code = form.cleaned_data['otp_code']
            # get the user id passed into the HTML
            user_id = request.POST.get("user_id", "0")
            
            # using the OTP code provided and the user id query the OTP table to see 
            # if there exists a record for the specified user with the specified OTP code
            saved_otp_code = OTP.objects.filter(user_id=user_id,otp_code=otp_code).count()

            # if the records are more than 0
            if saved_otp_code > 0:
                # user the user id to get the User from the table
                user = User.objects.get(pk=user_id)
                # log in this user (in the background)
                login(request, user)

                messages.success(request, f'Log In Successful')
                return redirect('home')
            
            messages.success(request, f'Invalid Code')
            return redirect('login')
    # if the request is a GET
    else:
        # get the id of the user who logged in
        user_id = request.user.id
        # get the phone number of the logged in user, which is stored in the Client table
        phone_number = Client.objects.filter(username=request.user.username).first().phone_number
        # invoke the get_code() method to generate and return a random string
        otp_code = get_code()

        # check if there is any OTP codes related to the currently logged in user in the OTP table
        otp_data = OTP.objects.filter(user=request.user)

        # if they are more than 0
        if otp_data.count() > 0:
            # delete all the related OTP codes
            otp_data.delete()
        
        # save the genertaed OTP code and related user in the OTP Table
        OTP.objects.create(user=request.user,otp_code=otp_code)

        # send the OTP code to the user's mobile phone
        send(phone_number=phone_number,message=f"Log In Code: {otp_code}")

        # generate the OTP form to be filled in by the user
        form = OTPForm()

        # log the user out (in the background), so that you can log them in once they enter correct OTP Password
        logout(request)

        # pass the OTP form and the user id into the HTML template as you won't access once you logout a user
        context = {'form': form, 'user_id': user_id}

    return render(request, 'users/otp.html', context)