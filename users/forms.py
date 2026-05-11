from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario de registro con validación de dominio institucional.
    """
    correo_institucional = forms.EmailField(
        label="Correo Institucional",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': f'usuario@{settings.INSTITUTIONAL_EMAIL_DOMAIN}',
            'required': True,
        })
    )
    
    first_name = forms.CharField(
        label="Nombre",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre',
        })
    )
    
    last_name = forms.CharField(
        label="Apellido",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido',
        })
    )
    
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña segura',
        })
    )
    
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
        })
    )
    
    class Meta:
        model = Usuario
        fields = ('correo_institucional', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_correo_institucional(self):
        """
        Valida que el correo sea del dominio institucional permitido.
        """
        correo = self.cleaned_data.get('correo_institucional').lower()
        
        # Validar dominio
        if not correo.endswith(f"@{settings.INSTITUTIONAL_EMAIL_DOMAIN}"):
            raise forms.ValidationError(
                f"Debes usar un correo del dominio @{settings.INSTITUTIONAL_EMAIL_DOMAIN}"
            )
        
        # Validar que no exista
        if Usuario.objects.filter(correo_institucional=correo).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado en el sistema"
            )
        
        return correo
    
    def clean_password2(self):
        """
        Valida que las contraseñas coincidan.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )
        
        if password1 and len(password1) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )
        
        return password2
    
    def save(self, commit=True):
        """
        Crea el usuario con el correo institucional y lo marca como no verificado.
        """
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data['correo_institucional'].split('@')[0]
        usuario.email = self.cleaned_data['correo_institucional']
        usuario.verificado = False
        
        if commit:
            usuario.save()
        
        return usuario


class VerificacionCodigoForm(forms.Form):
    """
    Formulario para verificar el código de 6 dígitos enviado por email.
    """
    correo_institucional = forms.EmailField(
        label="Correo Institucional",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu_email@uta.edu.ec',
            'readonly': 'readonly',
        }),
        help_text="El correo con el que te registraste"
    )
    
    codigo = forms.CharField(
        label="Código de Verificación",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '123456',
            'maxlength': '6',
            'inputmode': 'numeric',
        }),
        help_text="Ingresa el código de 6 dígitos que recibiste por email"
    )
    
    def clean_codigo(self):
        """
        Valida que el código contenga solo dígitos.
        """
        codigo = self.cleaned_data.get('codigo')
        
        if not codigo.isdigit():
            raise forms.ValidationError(
                "El código debe contener solo números"
            )
        
        return codigo
    
    def clean(self):
        """
        Valida que el usuario exista y el código sea correcto.
        """
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo_institucional', '').lower()
        codigo = cleaned_data.get('codigo')
        
        if not correo or not codigo:
            return cleaned_data
        
        try:
            usuario = Usuario.objects.get(correo_institucional=correo)
            
            if usuario.verificado:
                raise forms.ValidationError(
                    "Este usuario ya está verificado"
                )
            
            if not usuario.codigo_verificacion:
                raise forms.ValidationError(
                    "No hay código de verificación pendiente. Intenta registrarte de nuevo."
                )
            
            if usuario.codigo_verificacion != codigo:
                raise forms.ValidationError(
                    "El código es incorrecto"
                )
        
        except Usuario.DoesNotExist:
            raise forms.ValidationError(
                "Usuario no encontrado. Verifica que escribiste correctamente el correo."
            )
        
        return cleaned_data


class LoginUsuarioForm(forms.Form):
    """
    Formulario de login por correo institucional.
    """
    correo_institucional = forms.EmailField(
        label="Correo Institucional",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@uta.edu.ec',
        })
    )
    
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña',
        })
    )
    
    def clean_correo_institucional(self):
        """
        Normaliza el correo a minúsculas.
        """
        return self.cleaned_data.get('correo_institucional', '').lower()


# ============================================================================
# FORMULARIOS DE RECUPERACIÓN DE CONTRASEÑA
# ============================================================================

class SolicitarRecuperacionForm(forms.Form):
    """
    Formulario para solicitar la recuperación de contraseña.
    El usuario ingresa su correo institucional.
    """
    correo_institucional = forms.EmailField(
        label="Correo Institucional",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu_email@uta.edu.ec',
            'autofocus': True,
        }),
        help_text="Ingresa el correo con el que te registraste"
    )
    
    def clean_correo_institucional(self):
        """
        Valida que el usuario exista.
        """
        correo = self.cleaned_data.get('correo_institucional', '').lower()
        
        if not Usuario.objects.filter(correo_institucional=correo).exists():
            raise forms.ValidationError(
                "No encontramos una cuenta con este correo. Verifica que escribiste correctamente."
            )
        
        return correo


class VerificacionCodigoRecuperacionForm(forms.Form):
    """
    Formulario para verificar el código de recuperación.
    """
    correo_institucional = forms.EmailField(
        label="Correo Institucional",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu_email@uta.edu.ec',
            'readonly': 'readonly',
        }),
        help_text="El correo con el que solicitaste recuperar contraseña"
    )
    
    codigo = forms.CharField(
        label="Código de Recuperación",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '123456',
            'maxlength': '6',
            'inputmode': 'numeric',
            'autofocus': True,
        }),
        help_text="Ingresa el código de 6 dígitos que recibiste por email"
    )
    
    def clean_codigo(self):
        """
        Valida que el código contenga solo dígitos.
        """
        codigo = self.cleaned_data.get('codigo')
        
        if not codigo.isdigit():
            raise forms.ValidationError(
                "El código debe contener solo números"
            )
        
        return codigo


class CambiarContraseñaRecuperacionForm(forms.Form):
    """
    Formulario para cambiar la contraseña después de verificar el código.
    """
    correo_institucional = forms.EmailField(
        label="Correo Institucional",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        }),
        help_text="El correo asociado a tu cuenta"
    )
    
    nueva_contrasena = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña segura',
            'autofocus': True,
        }),
        help_text="Mínimo 8 caracteres"
    )
    
    confirmar_contrasena = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu nueva contraseña',
        }),
        help_text="Debe coincidir con la contraseña anterior"
    )
    
    def clean_nueva_contrasena(self):
        """
        Valida que la contraseña sea segura.
        """
        nueva_contrasena = self.cleaned_data.get('nueva_contrasena')
        
        if nueva_contrasena and len(nueva_contrasena) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )
        
        return nueva_contrasena
    
    def clean(self):
        """
        Valida que las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        nueva_contrasena = cleaned_data.get('nueva_contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')
        
        if nueva_contrasena and confirmar_contrasena:
            if nueva_contrasena != confirmar_contrasena:
                raise forms.ValidationError(
                    "Las contraseñas no coinciden"
                )
        
        return cleaned_data
