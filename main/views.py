from itertools import product
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Shop
import datetime, requests
from main.forms import ShopForm
from main.models import Shop
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags



# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        shop_list = Shop.objects.all()
    else:
        shop_list = Shop.objects.filter(user=request.user)

    context = {
        'applicationname' : 'Football Shop',
        'npm' : '2406345974',
        'name': 'Naufal Agam Ardiansyah',
        'class': 'PBP B',
        'shop_list' : shop_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def show_shop(request, id):
    shop = get_object_or_404(Shop, pk=id)

    context = {
        'shop': shop
    }

    return render(request, "shop_detail.html", context)

def show_xml(request):
     shop_list = Shop.objects.all()
     xml_data = serializers.serialize("xml", shop_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    shop_list = Shop.objects.all()
    data = [
        {
            'id' : shop.id,
            'name': shop.name,
            'price': shop.price,
            'description': shop.description,
            'category': shop.category,
            'thumbnail': shop.thumbnail,
            'shop_views': getattr(shop, 'shop_views', 0),
            'created_at': shop.created_at.isoformat() if shop.created_at else None,
            'is_featured': shop.is_featured,
            'user_id': shop.user.id if shop.user else None,
        }
        for shop in shop_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, shop_id):
   try:
       shop_item = Shop.objects.filter(pk=shop_id)
       xml_data = serializers.serialize("xml", shop_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Shop.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, shop_id):
    try:
        shop = Shop.objects.select_related('user').get(pk=shop_id)
        data = {
            'name': shop.name,
            'price': shop.price,
            'description': shop.description,
            'category': shop.category,
            'thumbnail': shop.thumbnail,
            'shop_views': getattr(shop, 'shop_views', 0),
            'created_at': shop.created_at.isoformat() if shop.created_at else None,
            'is_featured': shop.is_featured,
            'user_username': shop.user.username if shop.user_id else None,
        }
        return JsonResponse(data)
    except Shop.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
   
@csrf_exempt
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                "success": True,
                "message": "Akun berhasil dibuat!",
                "username": user.username
            }, status=201)
        else:
            # kirim pesan error validasi
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = JsonResponse({
                "success": True,
                "message": "Login berhasil!",
                "username": user.username
            }, status=200)
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
    else:
        form = AuthenticationForm(request)
        return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response   

def create_shop(request):
    form = ShopForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        shop_entry = form.save(commit = False)
        shop_entry.user = request.user
        shop_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_shop.html", context)

def edit_shop(request, id):
    shop = get_object_or_404(Shop, pk=id)
    form = ShopForm(request.POST or None, instance=shop)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_shop.html", context)

def delete_shop(request, id):
    shop = get_object_or_404(Shop, pk=id)
    shop.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_shop_entry_ajax(request):
    """
    Accept POST from AJAX form and create Shop entry.
    Expect fields: name, description, category, price, thumbnail, is_featured
    Return JsonResponse with created shop data (mapped to frontend keys).
    """
    # sanitize minimal input
    name = strip_tags(request.POST.get("name", "")).strip()
    description = strip_tags(request.POST.get("description", "")).strip()
    category = request.POST.get("category", "").strip()
    thumbnail = request.POST.get("thumbnail", "").strip()
    price = request.POST.get("price", None)
    # checkbox might be "on" or absent
    is_featured = request.POST.get("is_featured") in ("on", "true", "1")

    # Basic validation
    if not name or not description or not category or price is None:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Convert price to integer safely
    try:
        price_int = int(price)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid price'}, status=400)

    user = request.user if request.user.is_authenticated else None

    new_shop = Shop(
        name=name,
        description=description,
        category=category,
        thumbnail=thumbnail or None,
        is_featured=is_featured,
        price=price_int,
        user=user
    )
    new_shop.save()

    resp = {
        'id': new_shop.id,
        'title': new_shop.name,
        'content': new_shop.description,
        'category': new_shop.category,
        'thumbnail': new_shop.thumbnail,
        'shop_views': getattr(new_shop, 'shop_views', 0),
        'price': new_shop.price,
        'created_at': new_shop.created_at.isoformat() if new_shop.created_at else None,
        'is_featured': new_shop.is_featured,
        'user_id': new_shop.user.id if new_shop.user else None,
        'user_username': new_shop.user.username if new_shop.user else None,
    }

    return JsonResponse(resp, status=201)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = strip_tags(data.get("title", ""))  # Strip HTML tags
        content = strip_tags(data.get("content", ""))  # Strip HTML tags
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        user = request.user
        
        new_product = Shop(
            title=title, 
            content=content,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
def my_products_json(request):
    user = request.user
    items = Shop.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", items))
