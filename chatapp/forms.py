from django import forms
from .models import Conversation  # Import your Conversation model

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title', 'document']  # Include the 'title' field

    title = forms.CharField(max_length=100, label='Chat Title', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Chat Title'}))

    document = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'd-none', 'accept': '.zip,.rar,.7zip,.pdf,.txt,.html', 'multiple': ''}))
