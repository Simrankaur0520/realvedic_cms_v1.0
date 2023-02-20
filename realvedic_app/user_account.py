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
# from django.views.decorators.csrf import csrf_exempt
#----------------------------restAPI--------------------------------------------------
from rest_framework.decorators import parser_classes,api_view
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response

#----------------------------models---------------------------------------------------
from realvedic_app.models import user_data,user_address

#----------------------------extra---------------------------------------------------
import simplejson as json
import json


@api_view(['POST'])
def userAccountView(request,format=None):

    token=request.data['token']
    res={}
    user=user_data.objects.get(token=token)
    res['first_name']=user.first_name
    res['last_name']=user.last_name
    res['email']=user.email
    res['gender']=user.gender
    res['phone_code']=user.phone_code
    res['phone_no']=user.phone_no
    res['dob']=user.dob 
    try:
      
        user_address_val=user_address.objects.get(user_id=user.id)
      
        res['add_line_1']=user_address_val.add_line_1 
        res['add_line_2']=user_address_val.add_line_2
        res['city']=user_address_val.city
        res['landmark']=user_address_val.landmark
        res['state']=user_address_val.state
        res['country']=user_address_val.country
        res['pincode']=user_address_val.pincode
    except:
         
        res['add_line_1']=''
        res['add_line_2']=''
        res['city']=''       
        res['landmark']=''
        res['state']=''
        res['country']=''
        res['pincode']=''
        
    
    

    
    return Response(res)
@api_view(['POST'])
def UserAccountEdit(request,format=None):
    resp={}
    acc=request.data['data']
    
    token=request.data['token']
    res = json.loads(acc)
    
    first_name =res['first_name']
    last_name = res['last_name']
    gender = res['gender']
    dob = res['dob']
    email = res['email']
    phone_code = res['phone_code']
    phone_no = res['phone_no']
    
    #------------Address call
    add_line_1 = res['add_line_1']
    add_line_2 = res['add_line_2']
    landmark = res['landmark']
    city = res['city']
    state = res['state']
    country = res['country']
    pincode = res['pincode']
    user=user_data.objects.get(token=token)
    ua=user_address.objects.filter(user_id=user.id).values()
    if len(ua)==0:
        data=user_address(
                user_id=user.id,
                add_line_1=add_line_1,
                add_line_2=add_line_2,
                landmark=landmark,
                city=city,
                state=state,
                country=country,
                pincode=pincode)
        data.save()
        try:
            user_data.objects.filter(token = token).update(
                                                            first_name = first_name,
                                                            last_name= last_name,
                                                            email = email,
                                                            gender = gender,
                                                            dob = dob,
                                                            phone_code = phone_code,
                                                            phone_no = phone_no,
                                                        )
            resp = {
                'status':True,
                'message': 'Profile updated successfully'
                }
        except:
            resp = {
                    'status':user.id,
                    'message':ua.user_id
                }

    else:
            try:
                user_data.objects.filter(token = token).update(
                                                                first_name = first_name,
                                                                last_name= last_name,
                                                                email = email,
                                                                gender = gender,
                                                                dob = dob,
                                                                phone_code = phone_code,
                                                                phone_no = phone_no,
                                                            )
                user_address.objects.filter(user_id=user.id).update(
                                                                    add_line_1=add_line_1,
                                                                    add_line_2=add_line_2,
                                                                    landmark=landmark,
                                                                    city=city,
                                                                    state=state,
                                                                    country=country,
                                                                    pincode=pincode

                                                                    
                                                                        )
                resp = {
                    'status':True,
                    'message': 'Profile updated successfully'
                    }
            except:
                resp = {
                        'status':user.id,
                        'message':ua.user_id
                    }
   
    return Response(resp)
