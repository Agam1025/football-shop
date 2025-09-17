from django.shortcuts import render, redirect, get_object_or_404
from .models import Shop
from main.forms import ShopForm
from main.models import Shop
from django.http import HttpResponse
from django.core import serializers


# Create your views here.
def show_main(request):
    shop_list = Shop.objects.all()
    context = {
        'applicationname' : 'Football Shop',
        'npm' : '2406345974',
        'name': 'Naufal Agam Ardiansyah',
        'class': 'PBP B',
        'shop_list' : shop_list
    }

    return render(request, "main.html", context)

def create_shop(request):
    form = ShopForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_shop.html", context)

def show_shop(request, id):
    shop = get_object_or_404(Shop, pk=id)

    context = {
        'shop': shop
    }

    return render(request, "shop_detail.html", context)

def show_xml(request):
     news_list = Shop.objects.all()
     xml_data = serializers.serialize("xml", news_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = Shop.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, shop_id):
   try:
       shop_item = Shop.objects.filter(pk=shop_id)
       xml_data = serializers.serialize("xml", shop_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Shop.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, shop_id):
   try:
       shop_item = Shop.objects.get(pk=shop_id)
       json_data = serializers.serialize("json", [shop_item])
       return HttpResponse(json_data, content_type="application/json")
   except Shop.DoesNotExist:
       return HttpResponse(status=404)
   
# def add_employee(request):
#     employee = Employee.objects.create(
#         name=name,
#         age=age,
#         persona=persona
#     )
#     return HttpResponse(content = employee)