from django.urls import path
from docapp import views


urlpatterns = [
    path('', views.index, name="homepage"),
    path('ticket/<int:id>/', views.ticket_details, name="ticket_details"),
    path('user/<int:id>/', views.user_details, name="user_details"),
    path('ticketadd/', views.ticket_add_views, name="ticket_add_view"),
    path('useradd/', views.user_add_views, name="user_add_view"),
    path('login/', views.loginview),
    path('logout/', views.logoutview),
    path('ticket/edit/<int:id>/', views.ticket_edit_views, name="ticket_edit_view"),
    path('ticket/edit/invalid/<int:id>/', views.ticket_edit_invalid, name="ticket_edit_invalid"),
    path('ticket/edit/in_progress/<int:id>/', views.ticket_edit_in_progress, name="ticket_edit_in_progress"),
    path('ticket/edit/finished/<int:id>/', views.ticket_edit_finished, name="ticket_edit_finished"),
]
