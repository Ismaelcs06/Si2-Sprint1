# accounts/views.py
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django import forms

# Un form mínimo para crear roles (Group)
class RoleForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
        labels = {"name": "Nombre del rol"}

@login_required
@permission_required("auth.view_group", raise_exception=True)
def roles_list(request):
    roles = Group.objects.all().order_by("name")
    # Para mostrar contadores simples en la lista
    data = [
        {
            "id": r.id,
            "name": r.name,
            "num_perms": r.permissions.count(),
            "num_users": r.user_set.count(),
        }
        for r in roles
    ]
    return render(request, "accounts/roles.html", {"roles": data})

@login_required
@permission_required("auth.add_group", raise_exception=True)
def role_create(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:roles")
    else:
        form = RoleForm()
    return render(request, "accounts/roles_form.html", {"form": form})
