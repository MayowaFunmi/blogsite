from django import forms
from .models import Profile, City


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'gender', 'country', 'city', 'address', 'phone_number', 'profile_picture', 'interest', 'about_me']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Your Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Your Phone Number'}),
            'interest': forms.TextInput(attrs={'placeholder': 'What Topic(s) attract(s) You?'}),
            'about_me': forms.Textarea(attrs={'placeholder': 'Few Things About You...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


# login form
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
