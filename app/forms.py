from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app.models import Candidate, Comment, CustomUser, PoliticalParty, Race

class CandidateModelCreateForm(forms.ModelForm):  
    class Meta:
        model = Candidate
        exclude = ['up_users', 'down_users']

class CandidateModelUpdateForm(forms.ModelForm):  
    class Meta:
        model = Candidate
        exclude = ['up_users', 'down_users']


class CommentModelUpdateForm(forms.ModelForm): 
    class Meta:
        model = Comment
        fields = ('body', )


class CustomUserModelUpdateForm(UserChangeForm): 
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name')


class CustomUserCreateForm(UserCreationForm):
    """docstring for CustomUserCreateForm"""
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
        exclude = ['username']


class UserLogin(forms.Form):  
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput()) 
    next_page = forms.CharField(required=False, widget=forms.HiddenInput())


class CommentForm(forms.Form):
    body = forms.CharField(required=False, label="Enter your comment here!", widget=forms.Textarea(attrs={'id': 'comment_body', 'class': "form-control", 'placeholder':"Type your comment here"}))

class PoliticalPartyModelCreateForm(forms.ModelForm):  
    class Meta:
        model = PoliticalParty
        fields = '__all__'

class PoliticalPartyModelUpdateForm(forms.ModelForm): 
    class Meta:
        model = PoliticalParty
        fields = '__all__'


class RaceModelCreateForm(forms.ModelForm):  
    class Meta:
        model = Race
        fields = '__all__'

        
class RaceModelUpdateForm(forms.ModelForm): 
    class Meta:
        model = Race
        fields = '__all__'
