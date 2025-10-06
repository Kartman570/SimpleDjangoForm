from django.shortcuts import render


def user_form(request) -> render:
    return render(request, "app/user_form.html")
