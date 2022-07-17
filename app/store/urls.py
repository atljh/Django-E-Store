from django.urls import path
from . import views, cart
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.product_list, name='main'),
    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),
    path('cart/',  cart.cart_req, name='cart'),
    path('checkout/', views.checkout_req, name='checkout'),
    path('product/<int:product_id>/', views.product_req, name='product'),
    path('add/<int:product_id>/', cart.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', cart.remove_from_cart, name='remove_from_cart'),
    path('clearcart', cart.clear_cart, name='clear_cart'),
    path('category/', views.categories_req, name='categories'),
    path('category/<int:category_id>/', views.category_req, name='category'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_req, name='subcategory'),
    path('cabinet', views.cabinet_req, name='cabinet'),
    path('orders', views.orders_req, name='orders'),
    path('saveorder', views.save_order, name='save_order')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)