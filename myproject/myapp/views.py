from django.shortcuts import render
from .models import Records
import json
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Message
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Favorite
from .forms import MessageForm
from .models import Message
from .forms import FixerVisiteForm
from .forms import PredictionForm
from .utils import load_model
from .utils import load_model2
import pandas as pd
import numpy as np

def carte(request):
    records = Records.objects.filter(latitude__isnull=False, longitude__isnull=False)
    records_json = json.dumps(list(records.values('OBJECTID','latitude','Contact','Prix_de_vente', 'longitude','Type_de_bien','Name','Zone','Action_commerciale','Superficie','Nom_et_Prenom','Disponibilite')))
    return render(request, 'myapp/carte.html', {'records': mark_safe(records_json)})


def index(request):
    return render(request, 'myapp/index.html')

###def carte(request):
   ### return render(request, 'myapp/carte.html')

def biens(request):
    return render(request, 'myapp/biens.html')

def estimer(request):
    return render(request, 'myapp/estimer.html')

def connex(request):
    return render(request, 'myapp/connex.html')

def Appartements(request):
    return render(request, 'myapp/appartements.html')

def Villa(request):
    return render(request, 'myapp/Villa.html')



def custom_login(request):    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return render(request, 'myapp/connexion.html', {'error': 'Invalid credentials'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('myapp:profile')
        else:
            error = 'Invalid email or password'
            return render(request, 'myapp/connexion.html', {'error': error})
    return render(request, 'myapp/connexion.html')


def custom_logout(request):
    logout(request)
    return redirect('myapp:login')


@login_required
def profile(request):
    return render(request, 'myapp/profile.html')

@login_required
def fixer_visite_view(request):
    if request.method == 'POST':
        form = FixerVisiteForm(request.POST)
        zone = request.POST.get('zone')
        type_bien = request.POST.get('type_bien')

        if zone:
            form.fields['type_bien'].choices = [('', 'Sélectionner un type de bien')] + list(
                Records.objects.filter(Zone=zone).values_list('Type_de_bien', 'Type_de_bien').distinct()
            )
        if zone and type_bien:
            form.fields['etat'].choices = [('', 'Sélectionner une action commerciale')] + list(
                Records.objects.filter(Zone=zone, Type_de_bien=type_bien).values_list('Action_commerciale', 'Action_commerciale').distinct()
            )

        if form.is_valid():
            visite = form.save(commit=False)
            visite.user = request.user
            visite.save()
            messages.success(request, 'Votre visite a été fixée avec succès.')
            return redirect('myapp:fixer_visite')
        else:
            messages.error(request, 'Il y a eu une erreur avec votre soumission. Veuillez corriger les erreurs ci-dessous.')

    else:
        form = FixerVisiteForm()

    return render(request, 'myapp/fixer_visite.html', {'form': form})

def get_types_bien(request):
    zone = request.GET.get('zone')
    print("Zone reçue :", zone)
    if zone:
        types_bien = Records.objects.filter(Zone=zone).values_list('Type_de_bien', 'Type_de_bien').distinct()
        print("Types de bien renvoyés :", list(types_bien))
        return JsonResponse(list(types_bien), safe=False)
    else:
        return JsonResponse([], safe=False)

def get_etats(request):
    zone = request.GET.get('zone')
    type_bien = request.GET.get('type_bien')
    print("Zone et type bien reçus :", zone, type_bien)
    if zone and type_bien:
        etats = Records.objects.filter(Zone=zone, Type_de_bien=type_bien).values_list('Action_commerciale', 'Action_commerciale').distinct()
        print("États renvoyés :", list(etats))
        return JsonResponse(list(etats), safe=False)
    else:
        return JsonResponse([], safe=False)


@login_required
def user_settings(request):
    if request.method == 'POST':
        profile_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        profile_valid = profile_form.is_valid()
        password_valid = password_form.is_valid()

        if profile_valid:
            profile_form.save()
            messages.success(request, 'Vos coordonnées ont été mises à jour avec succès.')

        if password_valid:
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')

        if profile_valid or password_valid:
            return redirect('myapp:user_settings')

    else:
        profile_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    
    return render(request, 'myapp/user_settings.html', context)

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    admin_users = User.objects.filter(is_superuser=True)
    return render(request, 'myapp/inbox.html', {'messages': messages, 'admin_users': admin_users})

@login_required
def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'success': True, 'unread_count': unread_count})

@login_required
def mark_all_as_read(request):
    Message.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
    unread_count = 0
    return JsonResponse({'success': True, 'unread_count': unread_count})

@login_required
def unread_message_count(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    else:
        unread_count = 0
    return JsonResponse({'unread_count': unread_count})


@login_required
def delete_message(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        if not message_id:
            return JsonResponse({'success': False, 'message': 'Invalid message ID'})
        
        try:
            message = Message.objects.get(id=message_id, receiver=request.user)
            message.delete()
            return JsonResponse({'success': True})
        except Message.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Message does not exist'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def send_message(request):
    to_username = request.GET.get('to')
    recipient = None

    if to_username:
        recipient = get_object_or_404(User, username=to_username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient or form.cleaned_data['receiver']
            message.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})


@login_required()
def add_to_favorites(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        if not property_id:
            return JsonResponse({'success': False, 'message': 'Invalid property ID'})
        
        try:
            property_instance = Records.objects.get(OBJECTID=property_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_instance)
            if created:
                return JsonResponse({'success': True, 'message': 'Property added to favorites'})
            else:
                return JsonResponse({'success': False, 'message': 'Property already in favorites'})
        except Records.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Property does not exist'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def liked_properties(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'myapp/liked_properties.html', {'favorites': favorites})


@login_required
def remove_from_favorites(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        if not property_id:
            return JsonResponse({'success': False, 'message': 'Invalid property ID'})
        
        try:
            property_instance = Records.objects.get(OBJECTID=property_id)
            favorite = Favorite.objects.get(user=request.user, property=property_instance)
            favorite.delete()
            return JsonResponse({'success': True, 'message': 'Property removed from favorites'})
        except (Records.DoesNotExist, Favorite.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Property or favorite does not exist'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def is_authenticated(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


# Load the original CSV to get known categories
file_path = r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\Cleaned_DataFull1.csv'
original_data = pd.read_csv(file_path)
known_types = original_data['Type de bien'].unique()
known_addresses = original_data['Address'].unique()

# Function to preprocess the input data
import pandas as pd
import joblib



from django.shortcuts import render
from .utils import load_model
import pandas as pd

# Load the trained model
pipeline = joblib.load(r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\apps_model.joblib')

from django.shortcuts import render
from django.http import JsonResponse
import joblib
import pandas as pd
from .forms import PredictionForm

from django.shortcuts import render
from django.http import JsonResponse
import joblib
import pandas as pd
from .forms import PredictionForm

# Load the trained model
pipeline = joblib.load(r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\apps_model2.joblib')

# Load the data to get existing addresses
df = pd.read_csv(r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\updated_property_data.csv')
existing_addresses = df['Address'].tolist()

def predict_price(request):
    form = PredictionForm(request.POST or None, addresses=existing_addresses)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        
        # Calculate Surface per room
        surface_per_room = data['surface'] / data['nombre_de_chambres'] if data['nombre_de_chambres'] > 0 else 0
        data['surface_per_room'] = surface_per_room
        
        # Create a DataFrame from the form data
        input_data = pd.DataFrame([data], columns=['address', 'surface', 'nombre_de_chambres', 'nombre_de_toilettes', 'surface_per_room', 'year_of_construction', 'state'])
        
        # Rename columns to match those expected by the model
        input_data.rename(columns={
            'address': 'Address',
            'surface': 'Surface',
            'nombre_de_chambres': 'Nombre de chambres',
            'nombre_de_toilettes': 'Nombre de toilettes',
            'surface_per_room': 'Surface per room',
            'year_of_construction': 'Year of Construction',
            'state': 'State'
        }, inplace=True)
        
        print(input_data.columns)  # Debugging statement to check columns
        
        # Make prediction (drop the 'Address' column before prediction as it is not used by the model)
        prediction = pipeline.predict(input_data)
        
        # Return the prediction
        return render(request, 'myapp/appartements.html', {'form': form, 'prediction': prediction[0]})
    return render(request, 'myapp/appartements.html', {'form': form})

import pandas as pd
import joblib





from django.shortcuts import render
import joblib
import numpy as np
from .forms import PredictionForm
from django.http import HttpResponse


# Load the model when the server starts
model = joblib.load(r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\rent_price10.joblib')


def predict_price3(request):
    predicted_price4 = None
    if request.method == 'POST':
        # Extract features from POST request
        surface = float(request.POST.get('surface'))
        rooms = int(request.POST.get('rooms'))
        bathrooms = int(request.POST.get('bathrooms'))
        address = request.POST.get('address')

        # Create a DataFrame for the input data
        input_data = pd.DataFrame([[surface, rooms, bathrooms, address]],
                                  columns=['Surface', 'Nombre de Chambres', 'Nombre de Salles de Bain', 'Address'])

        # Predict the price using the pipeline
        predicted_price4 = model.predict(input_data)[0]

    return render(request, 'myapp/Louer.html', {'predicted_price4': predicted_price4})

from .forms import PredictionForm5
from .utils import preprocess_data5
model_filename = r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\classification3.joblib'
label_encoder_filename = r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\encoder_classification3.joblib'

model2 = joblib.load(model_filename)
label_encoder2 = joblib.load(label_encoder_filename)

csv_file_path = r'C:\Users\Asus PC\Downloads\projetfinal\myproject\myapp\static\myapp\models\updated_property_data2.csv'
property_data = pd.read_csv(csv_file_path)

# Assuming the CSV has a column named 'address'
property_addresses = property_data['Address'].unique()

def preprocess_input5(data):
    # One-hot encode categorical variables
    year_mapping = {
        'construction neuve': 'Year_of_Construction_construction neuve',
        'moins de 5 ans': 'Year_of_Construction_moins de 5 ans',
        'plus de 5 ans': 'Year_of_Construction_plus de 5 ans'
    }
    
    state_mapping = {
        'Luxe': 'State_Luxe',
        'normal': 'State_normal',
        'simple': 'State_simple'
    }
    address_mapping = {address: f'address_{address}' for address in property_addresses}
    # Convert the data into a DataFrame
    input_df = pd.DataFrame([data])
    
    for address, encoded in address_mapping.items():
        input_df[encoded] = (input_df['Address'] == address).astype(int)
    # Create a dictionary to map the original column names to one-hot encoded column names
    for original, encoded in year_mapping.items():
        input_df[encoded] = (input_df['Year_of_Construction'] == original).astype(int)
        
    for original, encoded in state_mapping.items():
        input_df[encoded] = (input_df['State'] == original).astype(int)
    
    # Drop the original categorical columns
    input_df.drop(columns=['Year_of_Construction', 'State'], inplace=True)
    
    # Ensure all necessary columns are present
    expected_columns = model2.feature_names_in_
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    return input_df[expected_columns]

def predict(request):
    prediction = None
    if request.method == 'POST':
        form = PredictionForm5(request.POST, addresses=property_addresses)
        if form.is_valid():
            input_data = form.cleaned_data
            input_data['Surface_per_Room'] = input_data['Surface'] / (input_data['Nombre_de_chambres'] + input_data['Nombre_de_toilettes'])
            print(f"Cleaned data: {input_data}")
            # Preprocess input data
            input_df = preprocess_input5(input_data)
            # Make prediction
            prediction = model2.predict(input_df)
            predicted_class = label_encoder2.inverse_transform(prediction)
            prediction = predicted_class[0]
    else:
        form = PredictionForm5()
    return render(request, 'myapp/classifier.html', {'form': form, 'prediction': prediction})