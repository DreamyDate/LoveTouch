from .models import Profile, Position
from .models import Profile
from django import forms
from django.contrib.auth.models import User
from .models import Profile, SocialLink, Status
from django.core.exceptions import ValidationError
import mimetypes
from .models import StatusComment, LanguageModel
from cities_light.models import Country, City

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full uk-scrollspy-inview',
        'id': 'email',
        'name': 'email',
        'type': 'email',
        'placeholder': 'Email',
    }))
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    
    # Добавляем новые поля
    gender = forms.ChoiceField(choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ], label='Gender')
    
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=range(1900, 2023)))
    
    relationship_goals = forms.ChoiceField(choices=[
        ('F', 'Friendship'),
        ('D', 'Dating'),
        ('R', 'Relationship'),
        ('N', 'Networking'),
    ], label='Relationship Goals')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'gender', 'date_of_birth', 'relationship_goals']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                         .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    def height_with_dot(self):
        return str(self.instance.height).replace(',', '.')
    def weight_with_dot(self):
        return str(self.instance.weight).replace(',', '.')
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    city = forms.CharField(max_length=100, required=False)

    def clean_city(self):
        city_name = self.cleaned_data.get('city')
        if city_name:
            try:
                city = City.objects.get(name=city_name)
                return city
            except City.DoesNotExist:
                raise forms.ValidationError('Invalid city selected.')
        return None


    class Meta:
        model = Profile
        fields = [f.name for f in Profile._meta.get_fields() if f.name not in ['following_set', 'initiated_matches','received_matches', 'credittransaction', 'premiumpurchase', 'night_mode', 'blocked_by']]
        exclude = ['user', 'relationship_goals', 'relationship_status', 'sexual_orientation', 'children', 'smoking', 'alcohol', 'physique', 'tatu', 'piercing', 'scars', 'zodiac_sign', 'animals', 'religion', 'interests', 'languages', 'school', 'education_level', 'work_and_education', 'organization', 'position', 'credits', 'notifications_enabled', 'language', 'timezone', 'followers', 'friends', 'liked_by', 'viewers', 'blocked_users', 'is_blocked', 'reason_for_blocking', 'night_mode', 'photo_verified', 'photo_verification_requested', 'last_activity', 'email_confirmed' ]


    
class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ('facebook', 'twitter', 'instagram')

class StatusForm(forms.ModelForm):
    file = forms.FileField(required=False)  # Одно поле для загрузки любого типа файла

    class Meta:
        model = Status
        fields = ('content', 'file', 'type')

    STATUS_TYPES_CHOICES = [
        ('text', 'Text'),
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]

    type = forms.ChoiceField(
        choices=STATUS_TYPES_CHOICES,
        widget=forms.Select(attrs={'class': 'selectpicker mt-2 story'})
    )

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if file:
            try:
                mime_type = mimetypes.guess_type(file.name)[0]  # Определение MIME-типа файла
                if mime_type.startswith('image'):
                    # Сохранение изображения
                    self.instance.photo = file
                elif mime_type.startswith('video'):
                    # Сохранение видео
                    self.instance.video = file
                else:
                    raise ValidationError("Invalid file type! Please upload an image or video.")
            except AttributeError:
                raise ValidationError("Couldn't read the file. Please try again.")

        return cleaned_data


class StatusCommentForm(forms.ModelForm):
    class Meta:
        model = StatusComment
        fields = ['text']


class ProfileEditRelationship(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['relationship_goals', 'relationship_status',
                  'sexual_orientation', 'children']


class ProfileAppearanceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['smoking', 'alcohol', 'physique', 'tatu', 'piercing', 'scars',
                  'zodiac_sign', 'animals', 'religion', 'interests', 'languages']

    languages = forms.ModelMultipleChoiceField(
        queryset=LanguageModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class ProfileEducationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'education_level',
                  'work_and_education', 'organization', 'position']
        
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(), required=False)



