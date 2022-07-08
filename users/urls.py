from django.urls import path, include
from users.views import home, about, otp, update_profile, ClientCreateView, account_created

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('account_created/', account_created, name='account_created'),

    path('login/', include([
        path('', auth_views.LoginView.as_view(template_name='users/login.html'), name = 'login'),
        path('login_redirect/', otp, name = 'login-redirect'),
    ])),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),

    path('client/', include([
        path('update/', update_profile, name = 'client-update'),
        path('register/', ClientCreateView.as_view(), name = 'client-add'),
    ])),


]