from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClienteSignupForm
from core.models import Customer

def signup(request):
    if request.method == 'POST':
        form = ClienteSignupForm(request.POST)
        
        if form.is_valid():
            # Se deu tudo certo
            print("----> FORMULÁRIO VÁLIDO! SALVANDO...") # Espião 1
            user = form.save()
            Customer.objects.create(
                user=user,
                name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                email=user.email
            )
            login(request, user)
            return redirect('home')
        else:
            # Se deu erro
            print("----> OPA! ERRO NO FORMULÁRIO:") # Espião 2
            print(form.errors) # <--- ISSO VAI MOSTRAR O ERRO NO TERMINAL
            
    else:
        form = ClienteSignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})