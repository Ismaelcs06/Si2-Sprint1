# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django import forms

# --------- Forms ----------
class RoleForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
        labels = {"name": "Nombre del rol"}


# --------- Vistas ----------
@login_required
@permission_required("auth.view_group", raise_exception=True)
def roles_list(request):
    """Lista de roles con contadores de permisos y usuarios."""
    roles = Group.objects.all().order_by("name")
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
    """Crear un nuevo rol."""
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:roles_list")
    else:
        form = RoleForm()
    return render(request, "accounts/roles_form.html", {"form": form, "title": "Nuevo rol"})


@login_required
@permission_required("auth.change_group", raise_exception=True)
def role_edit(request, pk: int):
    """Editar un rol existente."""
    role = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect("accounts:roles_list")
    else:
        form = RoleForm(instance=role)
    return render(request, "accounts/roles_form.html", {"form": form, "title": f"Editar: {role.name}"})


@login_required
@permission_required("auth.delete_group", raise_exception=True)
def role_delete(request, pk: int):
    """Confirmar y eliminar un rol."""
    role = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        role.delete()
        return redirect("accounts:roles_list")
    return render(request, "accounts/role_confirm_delete.html", {"role": role})
