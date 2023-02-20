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
from realvedic_app.models import user_data,user_address,PaymentOrder,Order_data
from realvedic_app.models import Product_data
from realvedic_app.models import user_cart

#----------------------------extra---------------------------------------------------
import simplejson as json

@api_view(['POST'])
def order_view(request,fromat=None):
    token=request.data['token']
    ord_lis=[]
    res={}
    all_order=[]
    #-----------------database data fetching -----------------------------------
    user=user_data.objects.get(token=token)
    ord=Order_data.objects.filter(user_id=user.id).values()
    user_address_val=user_address.objects.get(user_id=user.id)
    prods=ord.values('product_details')
    # for j in prods:
    #         ord_lis=eval(j['product_details']) 
    for i in ord:

            all_prod={
            'order_id': i['id'], 
            'status': i['status'] ,
            'items':eval(i['product_details']),
            'date': i['placed_at'], 
            'total_price':i['Total_amount']
            }
            all_order.append(all_prod)

        #res['items']=i['product_details']
    res['orders']=all_order
    return Response(res)

@api_view(['POST'])
def single_order_view(request,fromat=None):
    res={}
    order_details={}
    ord_lis=[]
    order_id=request.data['order_id']
    token=request.data['token']
     #-----------------database data fetching -----------------------------------
    user=user_data.objects.get(token=token)
    ord=Order_data.objects.filter(user_id=user.id,id=order_id).values()
    user_address_val=user_address.objects.get(user_id=user.id)
    prods=ord.values('product_details')
    for j in prods:
            ord_lis=eval(j['product_details']) 

    for i in ord :
        order_details={
            'status':i['status'],
            'items':ord_lis

        }
    item_total=ord.values_list('Total_amount',flat=True)
    total=""
    for i in item_total:
        total=i
    res['order_details']=order_details
    res['customer_name']=user.first_name + user.last_name
    res['phone_code']=user.phone_code
    res['phone_number']=user.phone_code
    res['address_line_1']=user_address_val.add_line_1 
    res['address_line_2']=user_address_val.add_line_2
    res['city']=user_address_val.city
    res['state']=user_address_val.state
    res['pincode']=user_address_val.pincode
    res['country']=user_address_val.country
    res['item_total']=int(total)
    res['delivery_charges']= '30'
    res['order_total']='570'

 
    return Response(res)


    '''
    required
    order_details : {
        status: 'Delivered',
        items: [
            { id: 0, title: 'Lemon Grass Rasam | Instant Mix', quantity: '1', weight: '250', price: '180', image: item },
            { id: 1, title: 'Garlic Rasam Powder | Instant Mix', quantity: '1', weight: '250', price: '180', image: item },
            { id: 2, title: 'Neem Flower Rasam | Instant Mix', quantity: '1', weight: '250', price: '180', image: item },
            { id: 3, title: 'Lemon Grass Rasam | Instant Mix ', quantity: '1', weight: '250', price: '180', image: item },
        ],
        customer_name: 'Vivek Khanal',
        phone_code: '+91',
        phone_number: '7784555487',
        address_line_1: 'Realvedic, 76, 7th B cross',
        address_line_2: 'Kormangla 4th B block',
        city: 'Bengaluru',
        state: 'Karnataka',
        pincode: '50306',
        country: 'India',
        item_total: '540',
        delivery_charges: '30',
        order_total: '570',
    },
white_check_mark
eyes
raised_hands
React
Reply

'''

    #order_details['status']=ord['status']
    '''for i in ord:
        prod=Product_data.objects.get(id=i['Product_id'])
        ord_data={
            'id':i['id'],
            'title':prod.title,
            'quantity':i['quantity'],
            'weight':i['size'],
            'price':i['price_per_unit'],
            'image':i['image']
        }
        ord_lis.append(ord_data)

        #-----------------Customer _details 
    res['customer_name']=user.first_name + user.last_name
    res['phone_code']=user.phone_code
    res['phone_number']=user.phone_code
    res['address_line_1']=user_address_val.add_line_1 
    res['address_line_2']=user_address_val.add_line_2
    res['city']=user_address_val.city
    res['state']=user_address_val.state
    res['pincode']=user_address_val.pincode
    res['country']=user_address_val.country'''
'''res['item_total']=
        res['delivery_charges']=
        res['order_total']='''

        
    

