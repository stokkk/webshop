from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

from operator import attrgetter
from .services import ServiceMain

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


# Create your views here.

app_name = 'main'

def index(request):
    products = ProductVar.objects.all()
    context = {'products': products, 'user': request.user}
    return render(request, 'main/index.html', context)


def product_detail(request, pk):
    context = ServiceMain.product_detail_context(request, pk=pk)
    return render(request, 'main/product_detail.html', context)
