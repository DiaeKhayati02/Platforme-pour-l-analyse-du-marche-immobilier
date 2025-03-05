from django.contrib import admin
from .models import Message
from .models import Records
from .models import Favorite
from .models import RDV
#username : root
#mdp : 12345

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('subject', 'body', 'sender__username', 'receiver__username')

@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    list_display = ('Type_de_bien', 'Zone', 'Name', 'Action_commerciale', 'Nom_et_Prenom', 'Superficie', 'Disponibilite', 'latitude', 'longitude', 'Contact', 'Prix_de_vente')
    search_fields = ('Type_de_bien', 'Zone')
    list_filter = ('Type_de_bien', 'Zone', 'Action_commerciale', 'Disponibilite')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'added_at')
    search_fields = ('user__username', 'property__title')


@admin.register(RDV)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('zone', 'type_bien', 'etat', 'telephone', 'email', 'date_visite', 'lien_bien', 'user')
    search_fields = ('zone', 'type_bien', 'etat', 'telephone', 'email', 'date_visite', 'lien_bien', 'user')