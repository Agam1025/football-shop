from django.urls import path
from main.views import show_main, create_shop, show_shop, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_shop, delete_shop, add_shop_entry_ajax, proxy_image, create_product_flutter, my_products_json

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-shop/', create_shop, name='create_shop'),
    path('shop/<str:id>/', show_shop, name='show_shop'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:shop_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:shop_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('shop/<int:id>/edit', edit_shop, name='edit_shop'),
    path('shop/<int:id>/delete', delete_shop, name='delete_shop'),
    path('add-shop-entry-ajax/', add_shop_entry_ajax, name='add_shop_entry_ajax'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_product_flutter, name='create_news_flutter'),
    path('my-products-json/', my_products_json, name='my_products_json'),

]

