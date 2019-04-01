from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm

urlpatterns = [
    path(
        'accounts/login/',
        auth_view.LoginView.as_view(
            template_name='authentication_login.html',
            authentication_form=LoginForm), name='login'),
    path(
        'logout',
        auth_view.LogoutView.as_view(next_page="login"),
        name='logout'),
    path(
        'edit-profile/<int:user_id>', views.edit_profile_view, name='edit_employee'),
    path(
        'product/<int:product_id>', views.product_view, name='product'),
    path(
        'product-detail/<int:product_id>', views.product_detail_view, name='product_detail'),
    path(
        'product-chat/<int:product_id>', views.registration_chat_view, name='registration_chat'),
    path(
        'product-chat/<int:product_id>-<int:user_id>', views.chat_view, name='chat'),
]
