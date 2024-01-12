from django import forms

# Creating a SignUp form
class SignupForm(forms.Form):
	email = forms.CharField(required=True, max_length = 30, widget=forms.TextInput(attrs={'placeholder':'Enter Your Email'}))
	username = forms.CharField(required=True, max_length = 15, widget=forms.TextInput(attrs={'placeholder':'Enter Your Username'}))
	password = forms.CharField(required=True, widget = forms.PasswordInput(attrs={'placeholder':'Enter Your Password'}))
	rePassword = forms.CharField(required=True, widget = forms.PasswordInput(attrs={'placeholder':'Enter The Password Again'}))
	fromGUI = forms.BooleanField(label="Is this request made from Browser", widget=forms.HiddenInput(), required=False, initial=False)

# Creating a Login form
class LoginForm(forms.Form):
  email = forms.CharField(required=True, max_length = 30, widget=forms.TextInput(attrs={'placeholder':'Enter Your Email'}))
  password = forms.CharField(required=True, widget = forms.PasswordInput(attrs={'placeholder':'Enter Your Password'}))
  fromGUI = forms.BooleanField(label="Is this request made from Browser", widget=forms.HiddenInput(), required=False, initial=False)