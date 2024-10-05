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
    path('session-delete/', views.sessionDelete, name="Session Delete"),
]
