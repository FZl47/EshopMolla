from django.shortcuts import render, HttpResponse, redirect, resolve_url
from FilterTags.templatetags.Filter import getCart, getWishList
from Transportation.models import Shipping
from User.models import User
from Product.models import Order, OrderDetail
from Config.Tools import Set_Cookie_Functionality, ValidationText, ValidationEmail, ValidationPassword , ValidationNumber
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login , logout
from Transportation.models import Address
import datetime


def dashboard(request):
    if request.user.id != None:
        context = {}
        context['User'] = request.user
        return render(request,'dashboard.html',context)
    return redirect('user:login_register')


def cart(request):
    context = {}
    context['Cart'] = getCart(request) or []
    context['Shippings'] = Shipping.objects.all()
    return render(request, 'cart.html', context)


def wishList(request):
    context = {}
    context['wishList'] = getWishList(request) or []
    return render(request, 'wishlist.html', context)


def proccedToCheckout(request):
    if request.user.id != None:
        if request.method == 'POST':
            data = request.POST
            shippingID = data.get('shipping')
            cart = request.user.getCart()
            shipping = Shipping.objects.filter(id=shippingID).first()
            if cart != None and shipping != None:
                try:
                    orderExists = Order.objects.filter(user_id=request.user.id, is_pay=False).first()
                    if orderExists != None:
                        # Delete past order
                        orderExists.delete()
                    # Create new order
                    order = Order.objects.create(user_id=request.user.id, shipping_id=shipping.id)
                    for detailCart in cart.getDetails():
                        countSeted = int(data.get(f"input-product-stock-{detailCart.id}"))
                        countStock = detailCart.productStock.count
                        if countSeted > countStock:
                            countSeted = countStock
                        detailCart.count = countSeted
                        detailCart.save()
                        # Create detail order
                        if countStock > 0:
                            detailOrder = OrderDetail.objects.create(order_id=order.id,
                                                                     product_id=detailCart.product.id,
                                                                     productStock_id=detailCart.productStock.id,
                                                                     count=detailCart.count,
                                                                     sizeText=detailCart.productStock.size.title,
                                                                     colorText=detailCart.productStock.color.name)
                    return redirect('user:checkout')
                except:
                    pass
            return Set_Cookie_Functionality('Cant find object Please inform support ', 'Error')
        raise PermissionDenied
    return redirect('user:login_register')


def checkout(reqeust):
    if reqeust.user.id != None:
        order = reqeust.user.getOrderActive()
        if order != None:
            context = {}
            context['Order'] = order
            context['Cart'] = reqeust.user.getCart()
            return render(reqeust, 'checkout.html', context)
        return redirect('user:cart')
    return redirect('user:login_register')


def proccedToPayment(request):
    if request.method == 'POST':
        if request.user.id != None:
            data = request.POST
            orderNote = data.get('orderNote')
            address = data.get('address') or 0
            paymentWay = data.get('paymentWay')  # Useless
            orderActive = request.user.getOrderActive()
            cart = request.user.getCart()
            address = Address.objects.filter(id=address,user_id=request.user.id).first()
            if address != None:
                if orderActive != None:
                    status = 200  # payment
                    if status == 200:
                        orderActive.is_pay = True
                        orderActive.priceShipping = orderActive.shipping.price
                        orderActive.priceProducts = orderActive.getPriceProducts()
                        orderActive.shippingText = orderActive.shipping.title
                        orderActive.total = orderActive.getPrice()
                        orderActive.dateTimePay = datetime.datetime.now()
                        orderActive.note = orderNote
                        orderActive.address = address
                        orderActive.addressText = address.getTextAddress()
                        orderActive.save()
                        cart.details.all().delete()
                    return Set_Cookie_Functionality('Order submited successfuly', 'Success',
                                                    RedirectTo=resolve_url('user:dashboard'))
                return Set_Cookie_Functionality('Active order not found','Error',RedirectTo=resolve_url('user:cart'))
            return Set_Cookie_Functionality('Address not found','Error',RedirectTo=resolve_url('user:cart'))
        return redirect('user:login_register')
    raise PermissionDenied


def login_register(request):
    if request.user.id == None:
        return render(request, 'login-register.html')
    return redirect('user:dashboard')


def register(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')
        if ValidationEmail(email, 5, 100) and ValidationPassword(password, 7, 64) and ValidationPassword(password2, 7,
                                                                                                         64):
            userExists = User.objects.filter(email=email).exists()
            if userExists == False:
                if password == password2:
                    user = User.objects.create_user(email=email, password=password)
                    cart = getCart(request)
                    wishlist = getWishList(request)
                    auth_login(request, user)
                    if cart != None:
                        cart.user_id = user.id
                        cart.save()
                    if wishlist != None:
                        wishlist.user_id = user.id
                        wishlist.save()
                    return Set_Cookie_Functionality('Your account was created successfully', 'Success',
                                                    RedirectTo=resolve_url('user:dashboard'))
                return Set_Cookie_Functionality('Passwords are not the same', 'Error')
            return Set_Cookie_Functionality('This is email is taken by another', 'Error')
        return Set_Cookie_Functionality('Please fill in the fields correctly', 'Error')
    raise PermissionDenied


def login(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember') or False
        if ValidationPassword(password, 7, 64) and ValidationEmail(email, 5, 100):
            user = User.objects.filter(email=email).first()
            if user != None and user.check_password(password) == True:
                if remember:
                    request.session.set_expiry(2592000)  # 2,592,000 Seconds = 1 Month
                else:
                    request.session.set_expiry(0)  # Sesstion

                sesstionCart = getCart(request)
                sesstionWishlist = getWishList(request)
                auth_login(request, user)
                userCart = user.getCart()
                userWishlist = user.getWishList()

                if userCart != None:
                    if sesstionCart != None:
                        userCart.details.add(*sesstionCart.details.all())
                        sesstionCart.delete()
                else:
                    if sesstionCart != None:
                        sesstionCart.user_id = user.id
                        sesstionCart.save()

                if userWishlist != None:
                    if sesstionWishlist != None:
                        userWishlist.details.add(*sesstionWishlist.details.all())
                        sesstionWishlist.delete()
                else:
                    if sesstionWishlist != None:
                        sesstionWishlist.user_id = user.id
                        sesstionWishlist.save()
                return Set_Cookie_Functionality('Welcome', 'Success', RedirectTo=resolve_url('user:dashboard'))
            return Set_Cookie_Functionality('Not found user with info', 'Error')
        return Set_Cookie_Functionality('Please fill in the fields correctly', 'Error')
    raise PermissionDenied


def logout_view(request):
    user = request.user
    if user != None:
        logout(request)
        return redirect('public:home')
    return redirect('user:login_register')



def submitInfo(request):
    user = request.user
    if request.method == 'POST' and user != None:
        context = {}
        data = request.POST
        first_name = data.get('first_name') or None
        last_name = data.get('last_name') or None
        phone_number = data.get('phone_number') or None
        if ValidationText(first_name,2,71) and ValidationText(last_name,2,71) and ValidationText(phone_number,10,12) and str(phone_number).isdigit():
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.save()
            return Set_Cookie_Functionality('Your info submited suceessfuly','Success')
        return Set_Cookie_Functionality('Please fill in the fields correctly', 'Error')
    raise PermissionDenied



def addAddress(request):
    user = request.user
    if request.method == 'POST' and user.id != None:
        data = request.POST
        city = data.get('city') or None
        postalCode = data.get('postalCode') or None
        address = data.get('address') or None
        if ValidationText(city,1,26) and ValidationText(address,2,501) and ValidationText(postalCode,2,26) and str(postalCode).isdigit():
            newAddress = Address.objects.create(user_id=user.id,city=city,postalCode=postalCode,address=address)
            return Set_Cookie_Functionality('Your address create successfuly','Success')
        return Set_Cookie_Functionality('Please fill in the fields correctly', 'Error')
    raise PermissionDenied



def changeAddress(request):
    user = request.user
    if request.method == 'POST' and user.id != None:
        data = request.POST
        city = data.get('city') or None
        postalCode = data.get('postalCode') or None
        address = data.get('address') or None
        addressID = data.get('addressID') or None
        if ValidationText(city,1,26) and ValidationText(address,2,501) and ValidationText(postalCode,2,26) and str(postalCode).isdigit() and addressID != None:
            getAddress = Address.objects.filter(id=addressID,user_id=user.id).first()
            getAddress.city = city
            getAddress.postalCode = postalCode
            getAddress.address = address
            getAddress.save()
            return Set_Cookie_Functionality('Your address changed successfuly','Success')
        return Set_Cookie_Functionality('Please fill in the fields correctly', 'Error')
    raise PermissionDenied



def getOrder(request,id):
    user = request.user
    if user.id != None:
        order = Order.objects.filter(id=id,user_id=user.id).first()
        if order != None:
            context = {}
            context['Order'] = order
            context['User'] = user
            return render(request,'order.html',context)
    return PermissionDenied


