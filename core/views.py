from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, Pet
from .forms import CustomerForm, PetForm

# --- PÁGINA INICIAL (DASHBOARD) ---
@login_required
def index(request):
    return render(request, 'index.html')

# --- MEUS PETS ---
@login_required
def my_pets(request):
    customer, created = Customer.objects.get_or_create(  # Tenta pegar o Customer ligado ao User, ou cria se não existir
        user=request.user,
        defaults={'name': request.user.username, 'email': request.user.email}
    )

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = customer # O dono é o usuário logado
            pet.save()
            return redirect('my_pets')
    else:
        form = PetForm()

    # Busca apenas os pets deste cliente
    pets = Pet.objects.filter(owner=customer)
    
    return render(request, 'core/my_pets.html', {'pets': pets, 'form': form})

# --- CADASTRO COMPLETO (Para Recepção/Admin) ---
@login_required
def customer_add(request):
    if request.method == 'POST':
        c_form = CustomerForm(request.POST)
        p_form = PetForm(request.POST, request.FILES)
        
        if c_form.is_valid() and p_form.is_valid():
            customer = c_form.save()
            pet = p_form.save(commit=False)
            pet.owner = customer
            pet.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
    else:
        c_form = CustomerForm()
        p_form = PetForm()

    return render(request, 'core/customer_form.html', {'c_form': c_form, 'p_form': p_form})

@login_required
def cadastrar_pet(request):
    # Tenta pegar o perfil do cliente logado
    try:
        cliente = request.user.customer
    except Customer.DoesNotExist:
        return redirect('signup') 

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = cliente           
            pet.save()                    
            return redirect('my_pets') # Redireciona para a lista de pets
    else:
        form = PetForm()

    return render(request, 'core/pet_form.html', {'form': form})