from django.db import models
from django.contrib.auth.models import User

class Records(models.Model):
    OBJECTID = models.AutoField(primary_key=True)
    Type_de_bien = models.CharField(max_length=100, default="Unknown type")
    Zone = models.CharField(max_length=100, default="Unknown Zone")
    Name = models.CharField(max_length=100, default="Unknown Name")
    Action_commerciale = models.CharField(max_length=100, default="Unknown Action")
    Nom_et_Prenom = models.CharField(max_length=100, default="Unknown Person", db_column='Nom_et_Prénom')
    Superficie = models.FloatField(default=0.0)
    Disponibilite = models.CharField(max_length=100, default="Unknown Availability", db_column='Disponibilité')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    Contact = models.FloatField(null=True, blank=True)
    Prix_de_vente = models.FloatField(null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
    

    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Records, to_field='OBJECTID', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    


class RDV(models.Model):
    zone = models.CharField(max_length=100)            
    type_bien = models.CharField(max_length=100)
    etat = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    date_visite = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lien_bien = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.zone} - {self.type_bien} - {self.etat}"




