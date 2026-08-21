from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Multiple AUTHENTICATION_BACKENDS configured (ModelBackend + allauth),
            # so Django needs to know explicitly which backend authenticated this user.
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "adminlte/auth/register.html", {"form": form})


def lockscreen(request):
    return render(request, "adminlte/auth/lockscreen.html")


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect("login")

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    next_url = request.GET.get("next") or "dashboard"

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect(next_url)
    else:
        form = UserCreationForm()
    return render(request, "adminlte/auth/register.html", {"form": form})


def lockscreen(request):
    return render(request, "adminlte/auth/lockscreen.html")