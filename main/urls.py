from django.urls import include, path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('category-list',views.category_list,name='category-list'),
    path('brand-list',views.brand_list,name='brand-list'),
    path('product-list',views.product_list,name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('brand-product-list/<int:brand_id>',views.brand_product_list,name='brand-product-list'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('accounts/signup',views.signup,name='signup'),
    path('add-wishlist',views.add_wishlist, name='add_wishlist'),
    path('my-wishlist',views.my_wishlist, name='my_wishlist'),
    path('checkout',views.checkout,name='checkout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset-confirm" ),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('my-dashboard',views.my_dashboard,name='my_dashboard'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)