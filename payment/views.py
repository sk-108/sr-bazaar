from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay

from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from store.models import Product

# Initialize Razorpay client
def get_razorpay_client():
    if not all([settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET]):
        raise ValueError("Razorpay credentials are not properly configured")
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@require_http_methods(["GET", "POST"])
def checkout(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart-summary')

    # Get shipping address if exists
    shipping_address = None
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()

    # Ensure Razorpay key is available
    razorpay_key = getattr(settings, 'RAZORPAY_KEY_ID', '')
    if not razorpay_key:
        messages.error(request, "Payment gateway is not properly configured. Please contact support.")
        return redirect('cart-summary')

    context = {
        'cart': cart,
        'shipping': shipping_address,
        'RAZORPAY_KEY_ID': razorpay_key,  # Make sure this matches exactly what's in the template
    }
    return render(request, 'payment/checkout.html', context)


@require_POST
def create_razorpay_order(request):
    try:
        data = json.loads(request.body)
        amount = int(float(data.get('amount', 0)) * 100)  # Convert to paise
        
        if amount <= 0:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        client = get_razorpay_client()
        
        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': amount,
            'currency': getattr(settings, 'PAYMENT_CURRENCY', 'INR'),
            'payment_capture': '1'  # Auto-capture payment
        })
        
        return JsonResponse({
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency']
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        try:
            # Get the webhook payload
            payload = json.loads(request.body)
            
            # Verify the webhook signature
            client = get_razorpay_client()
            client.utility.verify_webhook_signature(
                request.body.decode('utf-8'),
                request.headers.get('X-Razorpay-Signature', ''),
                settings.RAZORPAY_WEBHOOK_SECRET
            )
            
            # Handle different webhook events
            if payload.get('event') == 'payment.captured':
                # Handle successful payment
                payment_id = payload['payload']['payment']['entity']['id']
                order_id = payload['payload']['payment']['entity']['order_id']
                
                # Update your order status here
                # order = Order.objects.get(razorpay_order_id=order_id)
                # order.payment_status = 'completed'
                # order.save()
                
                return JsonResponse({'status': 'success'})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def complete_order(request):

    if request.POST.get('action') == 'post':

        name = request.POST.get('name')
        email = request.POST.get('email')

        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')

        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')


        # All-in-one shipping address

        shipping_address = (address1 + "\n" + address2 + "\n" +
        
        city + "\n" + state + "\n" + zipcode
        
        )

        # Shopping cart information 

        cart = Cart(request)


        # Get the total price of items

        total_cost = cart.get_total()


        '''

            Order variations

            1) Create order -> Account users WITH + WITHOUT shipping information
        

            2) Create order -> Guest users without an account
        

        '''

        # 1) Create order -> Account users WITH + WITHOUT shipping information

        if request.user.is_authenticated:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
            
            amount_paid=total_cost, user=request.user)


            order_id = order.pk

            for item in cart:

                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                
                price=item['price'], user=request.user)


        #  2) Create order -> Guest users without an account

        else:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
            
            amount_paid=total_cost)


            order_id = order.pk


            for item in cart:

                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                
                price=item['price'])



        order_success = True

        response = JsonResponse({'success':order_success})

        return response






    




def payment_success(request):


    # Clear shopping cart


    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]



    return render(request, 'payment/payment-success.html')







def payment_failed(request):

    return render(request, 'payment/payment-failed.html')










@csrf_exempt
def razorpay_verify(request):
    if request.method == 'POST':
        import json
        import hmac
        import hashlib
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        key_secret = bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8')
        msg = bytes(razorpay_order_id + '|' + razorpay_payment_id, 'utf-8')
        generated_signature = hmac.new(key_secret, msg, hashlib.sha256).hexdigest()
        if generated_signature == razorpay_signature:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure'}, status=400)
