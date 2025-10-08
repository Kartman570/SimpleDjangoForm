from django.http import HttpResponse
from django.shortcuts import render


def user_form(request) -> HttpResponse:
    """Render form for user registration"""
    return render(request, "app/user_form.html")
