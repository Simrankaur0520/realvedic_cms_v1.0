from django.contrib import admin
from django.urls import path
import realvedic_app.views as views 

from django.conf.urls.static import static
from django.conf import settings

import realvedic_app.auth as auth
#import realvedic_app.user_data as user
import realvedic_app.cart as cart
import realvedic_app.user_account as usr
import realvedic_app.paymentgateway as pay
import realvedic_app.doctors as doc
import realvedic_app.CartToOrder as cto
import realvedic_app.admin_pages.adminproductsInfo as ad
import realvedic_app.extra_functions as ex
'''import realvedic_app.admin_views as admin_views
import realvedic_app.payments as pay
import realvedic_app.order_status as od'''

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("write_data",views.write_data,name="write_data"),
    path("single_product_view",views.single_product_view,name="single_product_view"),
    path("categoryPage",views.categoryPage,name="categoryPage"),
    #path("all_product_view",views.all_product_view,name="all_product_view"),
    path("NavbarCategoryView",views.NavbarCategoryView,name="NavbarCategoryView"),
    path("search_bar",views.search_bar,name="search_bar"),

    #--------login and signup
    path('signUp',auth.signUp,name='signUp'),
    path('login',auth.login,name='login'),
    path('user_view',auth.user_view,name='user_view'),

    #-------cart----------------------
   
    path('add_to_cart',cart.add_to_cart,name='add_to_cart'),
    path('UserCartView',cart.UserCartView,name='UserCartView'),
    path('checkout',cart.checkout,name='checkout'),
    path('CartUpdate',cart.CartUpdate,name='CartUpdate'),
    path('CartitemDelete',cart.CartitemDelete,name='CartitemDelete'),


    #-------------------------------------------user details 
    path('userAccountView',usr.userAccountView,name='userAccountView'),
    path('UserAccountEdit',usr.UserAccountEdit,name='UserAccountEdit'),

    #---------------------------------Payment gateway------------------

    path('start_payment',pay.start_payment,name='start_payment'),
    path('handle_payment_success',pay.handle_payment_success,name='handle_payment_success'),
    #path('corder_view',pay.corder_view,name='corder_view'),



    path('doctor_detail_view',doc.doctor_detail_view,name='doctor_detail_view'),
    

    #-----------------------------Admin pages ------------------------------------------------

    path('adminProductView',ad.adminProductView,name='adminProductView'),
    path('adminProductEditView',ad.adminProductEditView,name='adminProductEditView'),
    

    #----------------------order pages--------------------------------

    path('order_view',cto.order_view,name='order_view'),
    path('single_order_view',cto.single_order_view,name='single_order_view'),

    #----------------------------------------------------------extra

    path('recently_viewed_oc',ex.recently_viewed_oc,name='recently_viewed_oc'),




    
    


]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
