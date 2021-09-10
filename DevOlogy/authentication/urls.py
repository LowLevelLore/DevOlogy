from django.urls import path
from django.contrib.auth import views as default_views
from .views import log_out_view, password_reset_request, user_data_deletion, fb_login_view, activate
from django.conf.urls import url, include

urlpatterns = [
    path("logout/", log_out_view, name='logout_view'),
    path("password/reset/", password_reset_request, name="password_reset"),
    path("password/reset/done",
         default_views.PasswordResetDoneView.as_view(template_name='auth/PasswordReset/password_reset_done.html'),
         name='password_reset_done_view'),
    path('password/reset/<uidb64>/<token>/',
            default_views.PasswordResetConfirmView.as_view(
                template_name="auth/PasswordReset/password_reset_confirm.html"),
            name='password_reset_confirm'),
    path('password/reset/complete/',
         default_views.PasswordResetCompleteView.as_view(
             template_name='auth/PasswordReset/password_reset_complete.html'),
         name='password_reset_complete'),
    url('social-core/', include('social_django.urls', namespace='social')),
    path('fb/user-data-deletion/', user_data_deletion),
    path('fb/login/done', fb_login_view),
    path('activate_account/<uidb64>/<token>/', activate, name="activate"),
    
]
