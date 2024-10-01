from django import forms
from .models import Book, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'published_year', 'num_pages', 'cover_image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'category': forms.Select(attrs={'class': 'border rounded p-2'}),
            'author': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'published_year': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
        }
        category = forms.ModelChoiceField(
            queryset=Category.objects.all(),  # ดึงข้อมูลหมวดหมู่ทั้งหมดจากฐานข้อมูล
            required=True,
            empty_label="เลือกหมวดหมู่"  # ให้แสดงข้อความเมื่อไม่มีการเลือก
        )

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-3 rounded-lg border', 'placeholder': 'อีเมล'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-3 rounded-lg border', 'placeholder': 'รหัสผ่าน'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'w-full p-3 rounded-lg border', 'placeholder': 'อีเมล'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('อีเมลนี้มีอยู่ในระบบแล้ว')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว')
        return username

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'border-gray-300 p-3 rounded-md'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']