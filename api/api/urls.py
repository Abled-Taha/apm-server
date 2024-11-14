from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="Home"),
    path('signin/', views.signin, name="Sign In"),
    path('signup/', views.signup, name="Sign Up"),
    path('docs/', views.docs, name="Docs"),
    path('vault-get/', views.vaultGet, name="Vault Get"),
    path('vault-new/', views.vaultNew, name="Vault New"),
    path('vault-edit/', views.vaultEdit, name="Vault Edit"),
    path('vault-delete/', views.vaultDelete, name="Vault Delete"),
    path('vault-import/', views.vaultImport, name="Vault Import"),
    path('session-get/', views.sessionGet, name="Session Get"),
    path('session-edit/', views.sessionEdit, name="Session Edit"),
    path('session-delete/', views.sessionDelete, name="Session Delete"),
    path('pp-get/', views.ppGet, name="PP Get"),
    path('pp-new/', views.ppNew, name="PP New"),
    path('otp-send/', views.otpSend, name="OTP Send"),
    path('otp-verify/', views.otpVerify, name="OTP Verify"),
]
