from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CustomUser
from django.contrib.auth import get_user_model
from .models import Profile, CustomUser

CustomUser = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Enter your CalPoly email")
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)
    graduating_class = forms.ChoiceField(choices=CustomUser.GRADUATING_CLASS_CHOICES)
    college = forms.ChoiceField(choices=CustomUser.COLLEGE_CHOICES)
    major = forms.CharField(label = 'Enter Major or "NA" if not applicable:', max_length=100)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'graduating_class', 'college', 'major']
        labels = {
            'username': 'Enter your Cal Poly username',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['graduating_class'].widget = forms.Select(choices=CustomUser.GRADUATING_CLASS_CHOICES)
        self.fields['graduating_class'].initial = '2027'
        self.fields['graduating_class'].widget.attrs['class'] = 'student-field'
        self.fields['major'].widget.attrs['class'] = 'student-field'






class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'graduating_class', 'college', 'major']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['graduating_class'].required = False
        if self.instance.user_type == 'faculty_staff':
            self.fields['graduating_class'].initial = 'not_applicable'
            self.fields['graduating_class'].widget.attrs['disabled'] = 'disabled'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']  # Add any other fields from your Profile model