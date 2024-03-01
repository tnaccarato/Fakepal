from django.contrib.auth.models import User
from payapp.models import Account
from django.shortcuts import render, redirect


def register(request):
    # If the request method is POST, user has submitted the form
    if request.method == 'POST':
        # Gets the data from the form
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Creates a new user with the data from the form
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        # Creates a new account for the user
        account = Account(user=user)
        account.save()
        return redirect('home')
    return render(request, 'register/register.html')
