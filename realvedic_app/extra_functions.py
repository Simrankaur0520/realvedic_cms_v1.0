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
import random


@api_view(['GET'])
def recently_viewed_oc(request,format=None):
    token = request.GET.get('token')
    try:
        user = user_data.objects.get(token = token)
        cart_product_ids = user_cart.objects.filter(user_id = user.id).values_list('product_id',flat=True)
    except:
        cart_product_ids = []
    products_list=[]
    prod=Product_data.objects.values('id','image','title','size','price').order_by('-id')[:4][::-1]
    
    
    #random_list.append(random.sample(prod,2))
    
    for i in prod:
        prods={
            'id':i['id'],
            'image':i["image"].split(',')[0],
            "title":i["title"],
            "weight":i["size"].split("|"),
            "price":i["price"].split("|")
        }
        if str(i['id']) in cart_product_ids:
                prods['cart_status'] = True
        else:
                prods['cart_status'] = False
    
       
        products_list.append(prods)

    return Response(products_list)

