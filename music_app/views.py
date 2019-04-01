from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ProfileForm,RegistrationCustomForm,MessegesForm
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

User = get_user_model()

# # Create your views here

@login_required
def chat_view(request, product_id,user_id):
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)
    messeges = Messeges.objects.prefetch_related('user','accepter').filter(product=product,user=user)
    form = MessegesForm(request.POST or None)
    if form.is_valid():
        new_disput = form.save(commit=False)
        text = form.cleaned_data['text']
        new_disput.text = text
        new_disput.user = request.user
        new_disput.accepter = product.user
        new_disput.product = product
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'chat-2.html', {'product':product,'messeges':messeges,'form': form})

def registration_chat_view(request, product_id):
    form = RegistrationCustomForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        phone_number = form.cleaned_data['phone_number']
        first_name = form.cleaned_data['first_name']
        new_user.username = phone_number
        new_user.first_name = first_name
        new_user.save()
        user = User.objects.get(id=new_user.id)
        if user:
            login(request, user)
            return HttpResponseRedirect(f'/{product_id}-{user.id}')
        else:
            print(login_user,'wronn')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {
        'form': form
    }
    return render(request, 'chat.html', context)

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'details.html', {'product': product})

@login_required
def edit_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form_user = ProfileForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user),
        instance=user)
    if form_user.is_valid():
        new_user = form_user.save()
        new_user.save()
        return HttpResponseRedirect(reverse('base'))
    context = {'form_user': form_user, 'user': user}
    return render(request, 'edit-profile.html', context)
