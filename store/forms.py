from django import forms
from django.contrib.auth import get_user_model

from .mail import send_mail_template
from .models import PasswordReset
from .utils import generate_hash_key

User = get_user_model()

class RegistrarForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmacion de contraseña", widget=forms.PasswordInput)
    # Comparar los Passwords
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('La Confirmacion no es correcta')
        return password2
    # Salvar el Password y todos los datos del modelo
    def save(self, commit=True):
        user = super(RegistrarForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    # Metodo de DJANGO que permite validar el Mail cuando ReserForm
    def clean_email(self):
        email = self.cleaned_data['email']
        # select * from User where email=email
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            "No existe usuario con ese Mail Imposiple cambiar pwd"
        )
    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'store/password_reset_mail.html'
        subject = 'Crear nueva contraseña en codigo virtual'
        context = {
            'reset': reset
        }
        send_mail_template(subject, template_name, context, [user.email])