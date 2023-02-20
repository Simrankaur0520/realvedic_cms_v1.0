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
from realvedic_app.models import user_cart,doctor_info

#----------------------------extra---------------------------------------------------
import simplejson as json


@api_view(['GET'])
def doctor_detail_view(request,format=None):
    obj=doctor_info.objects.values()
    res={}
    doct_list=[]
   
    #------------------------------------------------------assigning product_details to the response----------------------------------------------
    for i in obj:
        doct_dic={
            'id':i["id"],
            "title":i["title"],
            'education':i['education'],
            "experience":i["experience"],
            "speciality":i["speciality"],
            'available':i['available'],
            'images':i['image']

           }
        doct_list.append(doct_dic)
    
    return Response(doct_list)

