from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("roles/", views.roles_list, name="roles_list"),
    path("roles/nuevo/", views.role_create, name="role_create"),
]
