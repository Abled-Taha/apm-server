from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', views.signin, name="Sign In"),
    path('signup/', views.signup, name="Sign Up"),
    path('docs/', views.docs, name="Docs")
]
