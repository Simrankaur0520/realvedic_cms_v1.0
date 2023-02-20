import json
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password

# import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response

from realvedic_app.models import PaymentOrder,user_data,user_cart,Order_data,Product_data
from realvedic_app.serializers import OrderSerializer

# env = environ.Env()

# # you have to create .env file in same folder where you are using environ.Env()
# # reading .env file which located in api folder
# environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    amount = request.data['amount']
    name = request.data['name']
    token = request.data['token']

    client = razorpay.Client(auth=('rzp_test_gHJS0k5aSWUMQc', '8hPVwKRnj4DZ7SB1wyW1miaf'))
   
    #cart_to_order_shift(token)

    payment = client.order.create({"amount": eval(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    order = PaymentOrder.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'],
                                 token=token)

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""
    ord=PaymentOrder.objects.values()
    data = {
        "payment": payment,
        "order": serializer.data,
        "obj":ord
        
      
    }
    return Response(data)




@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    # print(type(request.data["response"]))
    res = eval(request.data["response"])
    token=request.data['token']
    final_price=request.data['amount']
    items=eval(request.data['items'])
    print(type(items))
  


    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id =""
    raz_pay_id = ""
    raz_signature = ""
    
    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]
       
       
    # get order by payment_id which we've created earlier with isPaid=False
    order = PaymentOrder.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=('rzp_test_gHJS0k5aSWUMQc', '8hPVwKRnj4DZ7SB1wyW1miaf'))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if not check:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()
    res=cart_to_order(token,items,ord_id,final_price)
    print(type(res))
    #cart_to_order_shift(token,amount,ord_id)
    

    res_data = {
        'message': 'payment successfully received!',
        
        'status':res
        
    }
 
  

    return Response(res_data)


def cart_to_order(token,items,ord_id,final_price):
   
    token=token
    items=items
    ord_id=ord_id
    res=""
    order_details=[]
    amount=final_price
    
    usr=user_data.objects.get(token=token)
    ord=PaymentOrder.objects.filter(token=token,order_payment_id=ord_id).values()
    prod=Product_data.objects.values()
  
    for i in range(len(ord)):
        if ord[i]['isPaid']==True:
                for i in range(len(items)):
                    prod_dict={
                        'Product_id':items[i]['product_id'],
                        'product_name':list(prod.filter(id=items[i]['product_id']).values_list('title',flat=True))[0],
                        'size':items[i]['size'],
                        'price_per_unit':items[i]['unit_price'],
                        'quantity':items[i]['quantity'],
                        'image':items[i]['image']

                    }
                    order_details.append(prod_dict)
                    cart=user_cart.objects.filter(user_id=usr.id,
                                                product_id=items[i]['product_id'],
                                        size=items[i]['size'],
                                        price_per_unit=items[i]['unit_price'],
                                        quantity=items[i]['quantity']).all()
                    cart.delete()
                    res='added successfully'
        else:
            res='something went wrong'
       

    data=Order_data(order_id=ord_id, 
                    user_id=usr.id,
                    product_details=list(order_details),
                    Total_amount=amount,
                    status='Placed'
    )

    data.save()
    return(res)
                  
                    
                                                    
   
''' usr=user_data.objects.get(token=token)
    items=items
    orde_id=ord_id
    print("return_type",type(items))'''
'''order_id=order_id
    if ord.isPaid==True:
        for i in items:
            order_data.objects.create(order_id=order_id, 
                                 user_id=usr.id, 
                                 Product_id=items[i]['product_id'],
                                 size=items[i]['size'],
                                 price_per_unit=items[i]['price_per_unit'],
                                 quantity=items[i]['quantity'])
        orde=order_data.objects.values()
        res={'added successfully'}

    else:
        res={'something went wrong'}'''

'''def corder_view(request,format=None):
 

    
   
 
    return HttpResponse(make_password('1234567890'))'''