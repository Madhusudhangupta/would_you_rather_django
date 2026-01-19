from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Question, Answer, User


class UserSignupForm(UserCreationForm):
    """Form for user registration with validation"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Enter your email'
        })
    )
    
    username = forms.CharField(
        max_length=150,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Choose a username (min 3 characters)'
        }),
        help_text='Username must be at least 3 characters long.'
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Enter password (min 8 characters)'
        }),
        help_text='Password must be at least 8 characters long.'
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Form for user login with enhanced validation"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Enter your password'
        })
    )
    
    error_messages = {
        'invalid_login': 'Please enter a correct username and password.',
        'inactive': 'This account is inactive.',
    }


class QuestionForm(forms.ModelForm):
    """Form for creating new questions"""
    
    class Meta:
        model = Question
        fields = ['option_one_text', 'option_two_text']
        widgets = {
            'option_one_text': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Enter option one',
                'name': 'optionOneText',
                'required': True
            }),
            'option_two_text': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Enter option two',
                'name': 'optionTwoText',
                'required': True
            }),
        }
        labels = {
            'option_one_text': 'Option One',
            'option_two_text': 'Option Two',
        }
    
    def clean_option_one_text(self):
        text = self.cleaned_data.get('option_one_text')
        if not text or len(text.strip()) < 3:
            raise ValidationError('Option one must be at least 3 characters long.')
        return text.strip()
    
    def clean_option_two_text(self):
        text = self.cleaned_data.get('option_two_text')
        if not text or len(text.strip()) < 3:
            raise ValidationError('Option two must be at least 3 characters long.')
        return text.strip()


class AnswerForm(forms.ModelForm):
    """Form for answering questions"""
    
    class Meta:
        model = Answer
        fields = ['option_selected']
        widgets = {
            'option_selected': forms.RadioSelect(attrs={
                'class': 'radio-option'
            }),
        }
        labels = {
            'option_selected': '',
        }