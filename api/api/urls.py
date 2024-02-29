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
]
