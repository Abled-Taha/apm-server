from django import forms

# creating a form 
class SignupForm(forms.Form):

	email = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'placeholder':'Enter Your Email'}))
	username = forms.CharField(max_length = 15, widget=forms.TextInput(attrs={'placeholder':'Enter Your Username'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder':'Enter Your Password'}))
	rePassword = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder':'Enter The Password Again'}))
	fromGUI = forms.BooleanField(label="Is this request made from Browser", widget=forms.HiddenInput(), required=False, initial=False)
