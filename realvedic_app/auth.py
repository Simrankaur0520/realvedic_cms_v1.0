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

#coment


@api_view(['POST'])
# @csrf_exempt
def signUp(request,format=None):
    if request.method == 'POST':
        gender = request.data['gender']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        dob = request.data['dob']
        phone_code = request.data['phone_code']
        phone_no = request.data['phone_no']
        password = request.data['password']

        enc_pass = make_password(password)
        token = make_password(email+password)

        if email in user_data.objects.values_list('email',flat=True):
            return Response({'message':'Email already exist',
                            'status':False    
                            })
        if phone_no in user_data.objects.values_list('email',flat=True):
            return Response({'message':'Phone number already exist',
                            'status':False 
                            })
        data = user_data(
                            first_name = first_name,
                            last_name = last_name,
                            email = email,
                            gender = gender,
                            dob = dob,
                            phone_code = phone_code,
                            phone_no = phone_no,
                            password = enc_pass,
                            token = token,
                        )
        data.save()
        
        res = { 
                'message':'User created successfully',
                'status':True    
        }   

        return Response(res)

@api_view(['GET'])
def user_view(request,format=None):
    obj=user_data.objects.values()
    user_address_val=user_address.objects.values()
    return Response(user_address_val)

@api_view(['POST'])
def login(request,format=None):
    email = request.data['email']
    password = request.data['password']

    try:
        user = user_data.objects.get(email = email)
        if check_password(password,user.password):
            res = {
                    'status':True,
                    'message':'login successfull',
                    'token':user.token
            }
        else:
            res = {
                    'status':False,
                    'message':'Invalid Credentials',
                  }
        return Response(res)
    except:
        res = {
                    'status':False,
                    'message':'Invalid Credentials',
                  }
        return Response(res)

        #nmgnfapdpdhotsyo