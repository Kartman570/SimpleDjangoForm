from django.shortcuts import render

def user_form(request):
    return render(request, "app/user_form.html")
