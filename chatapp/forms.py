from django import forms
from .models import Conversation  # Import your Conversation model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title', 'document']  # Include the 'title' field

    title = forms.CharField(max_length=100, label='Chat Title', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Chat Title'}))

    document = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'd-none', 'accept': '.zip,.rar,.7zip,.pdf,.txt,.html', 'multiple': ''}))


class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model=User
        fields=['old_password',"new_password1","new_password2"]

    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Old Password'})
    )
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pe-5','placeholder': 'Enter New Password'})
    )
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter Confirm Password'})
    )
    