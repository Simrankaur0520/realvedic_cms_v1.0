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
from realvedic_app.models import Product_data,categoryy,images_and_banners,blogs,user_cart
#from apiApp.models import user_whishlist,user_data
#from apiApp.models import metal_price,diamond_pricing


#----------------------------extra---------------------------------------------------
import simplejson as json

  
@api_view(['GET'])
def adminProductView(request,format=None):
    status= [{
        "name": "In stock",
        "color": "#00ac69"
        },
        {
        "name": "Out of stock",
        "color": "#FF0000"
        }
  ]
    res={}
    prod_list=[]
    titles=["Product ID", "Product Name", "Category"," HSN", "Stock", "Status","Actions"]

    prod_obj=Product_data.objects.values()
    for i in prod_obj:
        prods={
            'product_id':i['id'],
            'product_name':i["title"],
            "category":i["category"],
            "hsn":i["HSN"],
            "stock": 25,
            "status": "In stock"
        }
        prod_list.append(prods)
    res['titles']=titles
    res['content']=prod_list
    res['status']=status


    

    
    return Response(res)


@api_view(['GET'])
def adminProductEditView(request,format=None):
    #prod_id=request.data['token']
    Prod_id=10
    variant_data=[]
    res={}
    meta_fields_dict={}
    meta_fields=[]
    sibling_product={}
    #-------------------------------------------------------------
    prods_obj=Product_data.objects.values()
    prod=prods_obj.filter(id=Prod_id).values()
    single_prod_obj=prod[0]
    #-----------------------------------------------------------
    weights=single_prod_obj['size'].split('|')
    price=single_prod_obj['price'].split('|')
    sku=single_prod_obj['SKU'].split('|')
    #-----------------------------------------------------------
    sibling=single_prod_obj['sibling_product']
    siblingprod=prods_obj.filter(title=sibling).values()
    sibling_product['product_id']=siblingprod[0]['id']
    sibling_product['product_name']=siblingprod[0]['title']
    sibling_product['img']=siblingprod[0]['image']
    sibling_product['category']=siblingprod[0]['category']
    
    #-----------------------------------------------------------
    nutrition=single_prod_obj['nutrition'].split('|')
    nutritional_info=[
        {
       "n_name": "Total Fat",
       "n_value": nutrition[0],
       "n_unit": "g"
     },
     {
       "n_name": "Protien",
       "n_value": nutrition[1],
       "n_unit": "g"
     },
     {
       "n_name": "Carbohydrate",
       "n_value": nutrition[2],
       "n_unit": "g"
     },
     {
       "n_name": "Energy",
       "n_value": nutrition[3],
       "n_unit": "kcal"
     }]
    for i in range(len(weights)):
        variants_data= {
            'variant_name':weights[i],
            'price':price[i],
            'quantity':"",
            'sku':sku[i],

        }
        variant_data.append(variants_data)
    #--------------------------------------------------------
   
    meta_fields_dict['benefits']=single_prod_obj['benefits']        
    meta_fields_dict['ingredients']=single_prod_obj['ingredients']
    meta_fields_dict['how_to_use']=single_prod_obj['how_to_use']
    meta_fields_dict['how_we_make_it']=single_prod_obj['how_we_make_it']

#-----------------------------------------------------------    
    res['images']=single_prod_obj['image'].split(',')
    res['name']=single_prod_obj['title']
    res['id']= single_prod_obj['id']
    res['status']=single_prod_obj['Status']
    res['category']=single_prod_obj['category']
    res['hsn']=single_prod_obj['HSN']
    res['variant_data']=variant_data
    res['sibling_product']=sibling_product
    res['nutritional_info']=nutritional_info
    res['meta_fields']=meta_fields_dict
    
    #----------------------------------------------------------
    prod_category=prods_obj.values('category','HSN').distinct()
    #res['variant_dataa']=variants_data
    res['category_list']=prod_category

    #-------------------------------
    return Response(res)

def admin_product_edit_view(request,format=None):
    title=request.data['name']
    id=request.data['id']
    category=request.data['category']
    hsn=request.data['hsn']
    images=request.data['images']
    status=request.data['status']
    meta_fields=request.data['meta_fields']
    sibling_product=request.data['sibling_product']
    variant_data=request.data['variant_data']
    variant_name = (map(itemgetter('variant_name'), variant_data))
    size = '|'.join(list(variant_name))
    price_get = (map(itemgetter('price'), variant_data))
    price = '|'.join(list(price_get))
    SKU_get = (map(itemgetter('Sku'), variant_data))
    SKU = '|'.join(list(SKU_get))
    
    try:
        Product_data.objects.filter(id=id).update(title=title,
                                                category=category,
                                                HSN=hsn,
                                                image=images,
                                                status=status,
                                                benefits=meta_fields['benefits'],
                                                ingredients=meta_fields['ingredients'],
                                                how_to_use=meta_fields['how_to_use'],
                                                how_we_make_it=meta_fields['how_we_make_it'],
                                                sibling_product=sibling_product['product_name'],
                                                price=price,
                                                size=size,
                                                SKU=SKU,
        )
                                                
        
        res={
            'status':True,
            'message':"data updated successfully"
        }    
    except:
        
        res={
            'status':False,
            'message':"Something went wrong"
        }    

        return Response(res)



