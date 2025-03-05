from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('biens/', views.biens, name='biens'),
    path('estimer/', views.estimer, name='estimer'),
    path('connex/', views.connex, name='connex'),
    path('carte/', views.carte, name='show_records'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('fixer_visite/', views.fixer_visite_view, name='fixer_visite'),
    path('ajax/get_types_bien/', views.get_types_bien, name='get_types_bien'),
    path('ajax/get_etats/', views.get_etats, name='get_etats'),
    path('settings/', views.user_settings, name='user_settings'),
    path('inbox/', views.inbox, name='inbox'),
    path('send_message/', views.send_message, name='send_message'),
    path('inbox/mark-as-read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('inbox/mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('inbox/unread-count/', views.unread_message_count, name='unread_message_count'),
    path('delete_message/', views.delete_message, name='delete_message'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('liked_properties/', views.liked_properties, name='liked_properties'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('is_authenticated/', views.is_authenticated, name='is_authenticated'),
    path('appartements/', views.predict_price, name='appartements'),
    path('Louer/', views.predict_price3, name='Louer'),
    path('classifier/', views.predict, name='classifier'),
]