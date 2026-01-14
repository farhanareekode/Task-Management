from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import redirect_after_login


app_name = "accounts"
urlpatterns = [

    # MVT TEMPLATES
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redirect-after-login/', redirect_after_login, name='redirect-after-login'),
]
