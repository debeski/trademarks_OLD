from django import forms
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True, label="رقم الهاتف")
    occupation = forms.CharField(max_length=100, required=False, label="جهة العمل")
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Permissions"
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "occupation", "is_staff",  "permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude specific permissions from the available permissions list
        self.fields['permissions'].queryset = Permission.objects.exclude(codename__in=['add_logentry', 'change_logentry',
            'delete_logentry', 'view_logentry', 'add_theme', 'change_theme', 'delete_theme', 'view_theme', 'add_group',
            'change_group', 'delete_group', 'view_group', 'add_permission', 'change_permission', 'delete_permission',
            'view_permission', 'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
            'add_session', 'change_session', 'delete_session', 'view_session',
            'add_company', 'change_company', 'delete_company', 'view_company', 'add_country', 'change_country',
            'delete_country', 'view_country', 'add_catagory', 'change_catagory', 'delete_catagory', 'view_catagory',
            'add_doctype', 'change_doctype', 'delete_doctype', 'view_doctype', 'add_comtype', 'change_comtype', 'delete_comtype',
            'view_comtype',
        ])

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        user.user_permissions.set(self.cleaned_data["permissions"])
        return user

class CustomUserChangeForm(UserChangeForm):
    phone = forms.CharField(max_length=15, required=False, label="رقم الهاتف")
    occupation = forms.CharField(max_length=100, required=False, label="جهة العمل")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="كلمة المرور")
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Permissions"
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "occupation", "is_staff",  "permissions", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.exclude(codename__in=['add_logentry', 'change_logentry',
            'delete_logentry', 'view_logentry', 'add_theme', 'change_theme', 'delete_theme', 'view_theme', 'add_group',
            'change_group', 'delete_group', 'view_group', 'add_permission', 'change_permission', 'delete_permission',
            'view_permission', 'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype',
            'add_session', 'change_session', 'delete_session', 'view_session',
            'add_company', 'change_company', 'delete_company', 'view_company', 'add_country', 'change_country',
            'delete_country', 'view_country', 'add_catagory', 'change_catagory', 'delete_catagory', 'view_catagory',
            'add_doctype', 'change_doctype', 'delete_doctype', 'view_doctype', 'add_comtype', 'change_comtype', 'delete_comtype',
            'view_comtype',
        ])
        # Disable the superuser checkbox
        if "is_superuser" in self.fields:
            self.fields["is_superuser"].widget.attrs["disabled"] = True
            self.fields["is_superuser"].help_text = "Cannot be modified here."

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        user.user_permissions.set(self.cleaned_data["permissions"])
        return user

