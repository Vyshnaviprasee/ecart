from django.shortcuts import render

# Create your views here.

def show_accounts(request):

    return render(request, 'account.html')