from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ProfileForm
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

# # Create your views here

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})

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
