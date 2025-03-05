from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Message
from .models import Records
from .models import RDV





class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Nom', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Prenom', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Adresse email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Mot de passe actuel', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    new_password1 = forms.CharField(label='Nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    new_password2 = forms.CharField(label='Confirmer mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']
        receiver = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=True),
        label="Destinataire",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        label="Sujet",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    body = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )



class FixerVisiteForm(forms.ModelForm):
    class Meta:
        model = RDV
        fields = ['zone', 'type_bien', 'etat', 'telephone', 'email', 'date_visite', 'lien_bien']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['zone'] = forms.ChoiceField(
            choices=[('', 'Sélectionner une zone')] + list(Records.objects.values_list('Zone', 'Zone').distinct()), 
            required=True, 
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_zone'})
        )

        self.fields['type_bien'] = forms.ChoiceField(
            choices=[('', 'Sélectionner un type de bien')],  # Choix initial vide
            required=True,
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_type_bien'})
        )
        self.fields['etat'] = forms.ChoiceField(
            choices=[('', 'Sélectionner une action commerciale')],  # Choix initial vide
            required=True,
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_etat'})
        )

        self.fields['telephone'].widget.attrs.update({'class': 'form-control', 'id': 'id_telephone'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'id_email'})
        self.fields['date_visite'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_date_visite'
        })
        self.fields['lien_bien'].widget.attrs.update({'class': 'form-control', 'id': 'id_lien_bien'})



from django import forms

class PredictionForm(forms.Form):
    address = forms.CharField(label='Address', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surface = forms.FloatField(label='Surface', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    nombre_de_chambres = forms.IntegerField(label='Nombre de Chambres', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    nombre_de_toilettes = forms.IntegerField(label='Nombre de Toilettes', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    year_of_construction = forms.ChoiceField(
        choices=[
            ('construction neuve', 'Construction Neuve'),
            ('moins de 5 ans', 'Moins de 5 ans'),
            ('plus de 5 ans', 'Plus de 5 ans')
        ],
        label='Year of Construction',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    state = forms.ChoiceField(
        choices=[
            ('Luxe', 'Luxe'),
            ('normal', 'Normal'),
            ('simple', 'Simple')
        ],
        label='State',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.addresses = kwargs.pop('addresses', [])
        super(PredictionForm, self).__init__(*args, **kwargs)

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address not in self.addresses:
            raise forms.ValidationError('The entered address is not in the existing data.')
        return address


from django import forms

class PredictionForm5(forms.Form):
    Surface = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter surface area'
    }))
    Nombre_de_chambres = forms.IntegerField(label="Nombre de Chambres", widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter number of rooms'
    }))
    Nombre_de_toilettes = forms.IntegerField(label="Nombre de Toilettes", widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter number of toilets'
    }))
    
    YEAR_OF_CONSTRUCTION_CHOICES = [
        ('construction neuve', 'Construction Neuve'),
        ('moins de 5 ans', 'Moins de 5 ans'),
        ('plus de 5 ans', 'Plus de 5 ans')
    ]
    
    STATE_CHOICES = [
        ('Luxe', 'Luxe'),
        ('normal', 'Normal'),
        ('simple', 'Simple')
    ]
    
    Address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter address'
    }))
    Year_of_Construction = forms.ChoiceField(choices=YEAR_OF_CONSTRUCTION_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    State = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    def __init__(self, *args, **kwargs):
        self.addresses = kwargs.pop('addresses', [])
        super().__init__(*args, **kwargs)

    def clean_Address(self):
        Address = self.cleaned_data.get('Address')
        if Address not in self.addresses:
            raise forms.ValidationError(f"The address '{Address}' does not exist in the database.")
        return Address
    
    def as_dict(self):
        return {field.name: self.cleaned_data[field.name] for field in self}
