from django.urls import path, include
from django.urls import reverse_lazy
from .views import register, activate, home
from django.contrib.auth.views import PasswordChangeView, PasswordResetView,\
    PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView


urlpatterns = [
    path('register/', register, name='registrace'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('',home, name='home'),
    path('change-password/',PasswordChangeView.as_view(success_url=reverse_lazy('home'),
                              template_name='Atletika_Havirov/registration/change-password.html',

                                                       ),name='change_password'),
    path('password-reset/', PasswordResetView.as_view(
                              template_name='Atletika_Havirov/registration/password_reset_form.html',
                              subject_template_name='Atletika_Havirov/registration/password_reset_subject.txt',
                              email_template_name='Atletika_Havirov/registration/password_reset_email.html',
                                                      ), name='password_reset'),

    path('password-reset/done/',PasswordResetDoneView.as_view(
                              template_name='Atletika_Havirov/registration/password_reset_done.html',
                                                                ),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(
                              template_name='Atletika_Havirov/registration/password_reset_confirm.html',
                                                                ),name='password_reset_confirm'),

    path('password-reset-complete/', PasswordResetCompleteView.as_view(
                              template_name='Atletika_Havirov/registration/password_reset_complete.html',
                                                                ), name='password_reset_complete'),



]