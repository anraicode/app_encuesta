from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese Usuario',
            'maxlength': 20,
            'required': 'True'
        }
    ))
    clave = forms.CharField(label='Contraseña',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese Contraseña',
            'maxlength': 20,
            'required': True
        }
    ))

class RegistroForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese Nombre',
            'required': True
        }
    ))
    apellido = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese Apellido',
            'maxlength': 15,
            'required': True
        }
    ))
    correo = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Ingrese correo electronico',
            'required': True
        }
    ))
    usuario = forms.CharField(label='Usuario', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese Usuario',
            'maxlength': 15,
            'required': True
        }
    ))
    clave = forms.CharField(label='Contraseña',widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Ingrese Contraseña',
            'maxlength': 20,
            'required': True
        }
    ))