import numpy as np
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import re
from operator import itemgetter 
import os
import random
#-------------------------Django Modules---------------------------------------------
from django.http import Http404, HttpResponse, JsonResponse,FileResponse
from django.shortcuts import render
from django.db.models import Avg,Count,Case, When, IntegerField,Sum,FloatField,CharField
from django.db.models import F,Func,Q
from django.db.models import Value as V
from django.db.models.functions import Concat,Cast,Substr
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Min, Max
from django.db.models import Subquery
#----------------------------restAPI--------------------------------------------------
from rest_framework.decorators import parser_classes,api_view
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response

#----------------------------models---------------------------------------------------
from realvedic_app.models import user_data,user_address
from realvedic_app.models import Product_data
from realvedic_app.models import user_cart

#----------------------------extra---------------------------------------------------
import simplejson as json

#********************************************************************************************************************************

#------------------------------------------------Add To cart----------------------------------------------------------------------

#*********************************************************************************************************************************

 
@api_view(['POST'])
def add_to_cart(request,fromat=None):
     if request.method == 'POST':
        token = request.data['token']
        product_id = request.data['product_id']
        size = request.data['size']
        price=request.data['price']
        
        #----------------Checking produt data

        try:
            pro=Product_data.objects.get(id=product_id)
            print("1st try encounetred")
            try:
                user = user_data.objects.get(token = token)
                print("2nd try encounetred")
            except:
                res = {
                        'status':False,
                        'message':'Something went wrong'
                    }
                return Response(res)
            obj = user_cart.objects.filter(user_id = user.id,
                                        product_id = product_id,
                                        price_per_unit=price,
                                        size = size
                                        ).values()
            if len(obj) == 0:
                data = user_cart(
                                    user_id = user.id,
                                    product_id = product_id,
                                    size = size,
                                    price_per_unit=price,
                                    quantity = '1',
                                    image=pro.image
              
                                )
                data.save()
               
                res = {
                        
                        'status' : True,
                        'message': 'Product added to cart successfully'
                    }
                return Response(res)
            else:
                obj = user_cart.objects.filter(user_id = user.id,
                                        product_id = product_id,
                                        size = size,
                                        price_per_unit=price).values().last()
                quantity = int(obj['quantity'])+1
                user_cart.objects.filter(user_id = user.id,
                                        product_id = product_id,
                                        size = size,
                                        price_per_unit=price,
                                       ).update(quantity = quantity)
                res = {
                        'status' : True,
                        'message': 'Product already exist, quantity increased'
                    }
                return Response(res)
                    

        #---------------Except block for product id to perform further actions
        except:
            res = {
                    'status':False,
                    'message':'Something went wrong'
                }
            return Response(res)


#********************************************************************************************************************************

#------------------------------------------------UserCartView----------------------------------------------------------------------

#*********************************************************************************************************************************


@api_view(['POST'])
def UserCartView(request,format=None):
    token = request.data['token']
    #--------------------variables for calculations----------
    subtotal=0
    shipping=40
    tax=50
    final_price=0
    #------------------------
    cartitems=[]
    res={}
    
    try:
        user = user_data.objects.get(token = token)
 
    except:
        res = {
                'status':False,
                'message':'Something went wrong'
            }
        return Response(res)
    
    items = user_cart.objects.filter(user_id = user.id).values()

    for i in items:
        products = Product_data.objects.filter(id=i['product_id']).values()
        for j in products:
            subtotal=subtotal+eval(i['price_per_unit'])*eval(i['quantity'])
            prod_dict={
                'product_id':i['product_id'],
                'name':j['title'],
                'size':i['size'],
                'unit_price':i['price_per_unit'],
                'price':eval(i['price_per_unit'])*eval(i['quantity']),
                'quantity':i['quantity'],
                'image':j['image'].split(',')[0]
            }
            #subtotal=subtotal+eval(prod_dict['price'])
            cartitems.append(prod_dict)


    final_price=subtotal+tax+shipping
    cart_total={
        'subtotal':subtotal,
        'shipping':shipping,
        'tax':tax,
        'final_price':final_price


    }    
   
    if len(items)==0:
        res = {
            'status':True,
            'message':'Cart generated successfully',
            'cartItems':[],
            'cart_total': []
          }
        return Response(res)
    else :
        res['cartItems']=cartitems
        res['cart_total']=cart_total



        return Response(res)

#********************************************************************************************************************************

#------------------------------------------------checkout----------------------------------------------------------------------

#*********************************************************************************************************************************

 

@api_view(['POST'])
def checkout(request,format=None):
    token=request.data['token']
     
    #--------------------variables for calculations----------
    subtotal=0
    shipping=40
    tax=50
    final_price=0
    #------------------------
    cartitems=[]
    
    
    res={}
    try:
        user = user_data.objects.get(token = token)
        items = user_cart.objects.filter(user_id = user.id).values()
        #products = Product_data.objects.filter(id=items.product_id).values()
        for i in items:
            products = Product_data.objects.filter(id=i['product_id']).values()
            for j in products:
                subtotal=subtotal+eval(i['price_per_unit'])*eval(i['quantity'])
                prod_dict={
                    'product_id':i['product_id'],
                    'name':j['title'],
                    'size':i['size'],
                    'unit_price':i['price_per_unit'],
                    'price':eval(i['price_per_unit'])*eval(i['quantity']),
                    'quantity':i['quantity'],
                    'image':j['image']
                }
                
                cartitems.append(prod_dict)


        final_price=subtotal+tax+shipping
        
        address=user_address.objects.get(user_id=user.id)
        personal_info={
            "first_name":user.first_name,
            'last_name':user.last_name,
            "email":user.email,
            "phone_code":user.phone_code,
            "phone_number":user.phone_no
        }
        address_info={
            "address_line_1":address.add_line_1,
            "address_line_2":address.add_line_2,
            'landmark':address.landmark,
            "city":address.city,
            "state":address.state,
            "pincode":address.pincode,
            "country":address.country
        }

        res['personal_info']=personal_info
        res['address_info']=address_info
        res['items']=cartitems
        res['item_total']=subtotal
        res['shipping']=shipping
        res['tax']=tax
        res['final_price']=final_price


        
        return Response(res)
    except:
            res={
                    'status':False,
                    'message':"Something went wrong"
                }

            return Response(res)

#********************************************************************************************************************************

#------------------------------------------------CartUpdate----------------------------------------------------------------------

#*********************************************************************************************************************************

@api_view(['POST'])
def CartUpdate(request,format=None):
    token=request.data['token']
    update_type=request.data['update_type']
    prod_id=request.data['prod_id']
    size=request.data['size']
    price=request.data['price']



    #----------------------data fetching-----------------------
    
    user = user_data.objects.get(token = token)
    items = user_cart.objects.filter(user_id = user.id,product_id=prod_id,size=size,price_per_unit=price).values().values()
        #item_to_be_updated=items.filter(product_id=prod_id).values('quantity')
    for i in items :
        quantity=int(i['quantity'])
   
        if update_type=='+':
                    quantity=quantity+1
                    user_cart.objects.filter(user_id = user.id,product_id=prod_id,size=size,price_per_unit=price).update(quantity=quantity)
                    res={
                        'status':True,
                        'message':"Product quantity increased successfully",
                        'items' :user_cart.objects.filter(user_id = user.id).values()

                    }
        elif update_type=="-":
            
                    quantity=quantity-1
                    if quantity<=0:
                        
                        dell=user_cart.objects.get(user_id = user.id,product_id=prod_id,size=size,price_per_unit=price)
                        
                        dell.delete()
                        
                        res={
                        'status':True,
                        'message':"Product Deleted from cart",
                        'items' :user_cart.objects.filter(user_id = user.id).values()

                    }
                    else:
                        user_cart.objects.filter(user_id = user.id,product_id=prod_id,size=size,price_per_unit=price).update(quantity=quantity)

                        res={
                            'status':True,
                            'message':"Product quantity decreased successfully",
                            'items' :user_cart.objects.filter(user_id = user.id).values()

                        }
        else:
                    res={
                        'status':False,
                        'message':"Something went wrong",
                        'items' :user_cart.objects.filter(user_id = user.id).values()

                    }
    '''except:
            res={
                    'status':False,
                    'message':"Something went wrong"
                }
    except:
            res={
                    'status':False,
                    'message':"Something went wrong"
                }'''

            
    return Response(res)

#********************************************************************************************************************************

#------------------------------------------------CartitemDelete----------------------------------------------------------------------

#*********************************************************************************************************************************


@api_view(['POST'])
def CartitemDelete(request,format=None):
    token=request.data['token']
    prod_id=request.data['prod_id']
    size=request.data['size']
    price=request.data['price']
  
    #----------------------data fetching-----------------------
    try:
        user = user_data.objects.get(token = token)
        items = user_cart.objects.get(user_id = user.id,product_id=prod_id,size=size,price_per_unit=price)
        items.delete()
        res={
            'status':True,
            "message":"item deleted successfully"
        }
    except:
        res={
            'status':False,
            "message":"something went wrong"
        }
    return Response(res)
    

