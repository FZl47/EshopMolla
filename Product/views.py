from django.shortcuts import render, Http404, redirect, resolve_url, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic import View
from User.models import User
from django.db.models import Value, Max, F, Case, When, Sum, Q
from Product.models import *
from django.core.paginator import Paginator
from django.db import connection, reset_queries
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from Config.Tools import Distinct, ListIsNone, Set_Cookie , Set_Cookie_Functionality
import math , json


def getProductPagination(req, listProducts):
    step = 4  # How many products to display

    def noneVal():
        pagination = Paginator([], step)
        pagination.currentPage = 1
        pagination.step = step
        return [], pagination.get_page(1), pagination
    numberPage = req.GET.get('page') or 1
    pagination = Paginator(listProducts, step)
    try:
        numberPage = int(numberPage)
        if numberPage < 1:
            numberPage = 1
        pagination.currentPage = numberPage
        pagination.step = step
        pagination.countPages = int(math.ceil((len(listProducts) / step)))
        pagination.lastPage = pagination.countPages
        listRange = []
        if numberPage - 1 > 1:
            listRange.append(numberPage - 1)
        for i in range(numberPage, numberPage + 3):
            if i < pagination.lastPage and i > 1:
                listRange.append(i)
        pagination.listRange = listRange
    except:
        return noneVal()
    if numberPage <= pagination.num_pages:
        getPage = pagination.get_page(numberPage)
        return getPage.object_list, getPage, pagination
    return noneVal()

def handle_filter_products(request,context,getProducts):
    # Search Products
    searchIsActive = request.GET.get('search') or False
    if searchIsActive:
        context['searchIsActive'] = True
        context['searchContent'] = searchIsActive
        if str(searchIsActive).isdigit():
            lookUp = Q(title__icontains=searchIsActive) | Q(price=searchIsActive) | Q(
                categories__title__icontains=searchIsActive)
        else:
            lookUp = Q(title__icontains=searchIsActive) | Q(categories__title__icontains=searchIsActive)
        getProducts = getProducts.filter(lookUp)

    # Filter Products
    getCategories = Category.objects.all()
    getBrands = Brand.objects.all()
    getColors = Color.objects.all()
    highsetPriceProduct = math.ceil(getProducts.aggregate(highsetPrice=Max('price'))['highsetPrice'] or 1)
    rangePriceFilter = f'0-{highsetPriceProduct}'

    filterIsActive = request.GET.get('filter') or False

    def getListValueFilter(strList):
        # list with string => [name-1,name-2] => number is pk
        if strList:
            try:
                strList = str(strList).split('_')
                if type(strList) == list:
                    strList = [int(i.split('-')[-1]) for i in strList]
                    return strList
            except:
                pass
        return None

    if filterIsActive == 'true':
        filter_categories = request.GET.get('cats') or False
        filter_brands = request.GET.get('brands') or False
        filter_colors = request.GET.get('colors') or False
        filter_range = request.GET.get('range') or False

        filter_categories = getListValueFilter(filter_categories)
        if filter_categories == None:
            filter_categories = getCategories.values_list('id')

        filter_colors = getListValueFilter(filter_colors)
        if filter_colors == None:
            filter_colors = getColors.values_list('id')

        filter_brands = getListValueFilter(filter_brands)
        if filter_brands == None:
            filter_brands = getBrands.values_list('id')

        if filter_range:
            try:
                filter_range = str(filter_range)
                priceStart = filter_range.split('-')[0]
                priceEnd = int(filter_range.split('-')[-1])
            except:
                priceStart = 0
                priceEnd = int(highsetPriceProduct)
        else:
            priceStart = 0
            priceEnd = int(highsetPriceProduct)
        rangePriceFilter = f"{priceStart}-{priceEnd}"

        # Filter products
        try:
            getProducts = getProducts.filter(categories__in=filter_categories,
                                             productStock__color__in=filter_colors, productStock__count__gt=0,
                                             brand__in=filter_brands, price__gte=priceStart, price__lte=priceEnd)
        except:
            pass

    # May not be in the number list => filter_categories ==> [1,3,5,"ali"] : raise Error
    try:
        getCategories = getCategories.annotate(
            filterCategorySelected=Case(When(pk__in=filter_categories, then=Value(True))))
    except:
        getCategories = getCategories.annotate(filterCategorySelected=Value(True))
    try:
        getColors = getColors.annotate(filterColorSelected=Case(When(pk__in=filter_colors, then=Value(True))))
    except:
        getColors = getColors.annotate(filterColorSelected=Value(True))
    try:
        getBrands = getBrands.annotate(filterBrandSelected=Case(When(pk__in=filter_brands, then=Value(True))))
    except:
        getBrands = getBrands.annotate(filterBrandSelected=Value(True))

    # Order
    # By default ordered by popularity
    getProducts = getProducts.distinct()
    orderBy = request.GET.get('orderby') or 'popularity'
    if orderBy == 'popularity':
        getProducts = orderByPopulariy(getProducts)
    elif orderBy == 'date':
        getProducts = orderByDate(getProducts)
    elif orderBy == 'price':
        getProducts = orderByPrice(getProducts)
    else:
        # If it reaches this part : orderByID => show latest
        pass

    # Pagination
    context['countAllProduct'] = len(getProducts)
    resultProducts, pageActive, pagination = getProductPagination(request, getProducts)

    # Response
    context['highsetPriceProduct'] = highsetPriceProduct
    context['rangePriceFilter'] = rangePriceFilter
    context['categories'] = getCategories
    context['brands'] = getBrands
    context['colors'] = getColors
    context['products'] = resultProducts
    context['countProducts'] = len(resultProducts)
    context['showingProducts'] = pagination.currentPage * pagination.step
    context['filterIsActive'] = filterIsActive
    context['pageActive'] = pageActive
    context['pagination'] = pagination
    return context

class products(View):
    template_name = 'Products/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        getProducts = Product.getProducts.select_related('brand').prefetch_related('categories').all()
        context = handle_filter_products(request,context,getProducts)

        return render(request, self.template_name, context)


def getProductBySlug(request, slug):
    try:
        product_id = str(slug).split('-')[-1]
        product = Product.objects.get(product_id=product_id,status_show='active')
        return product
    except:
        raise Http404

def getCategoryByTitle(request,title):
    try:
        category = Category.objects.get(title__exact=title)
        return category
    except:
        raise Http404

class product(View):
    template_name = 'Product/index.html'

    def get(self, request, slug):
        context = {
            'product': getProductBySlug(request, slug)
        }
        return render(request, self.template_name, context)


class category(View):
    template_name = 'Products/Category.html'

    def get(self,request,title):
        context = {}
        getCategory = getCategoryByTitle(request,title)
        context['Category'] = getCategory
        getProducts = Product.getProducts.filter(categories__in=[getCategory])
        context = handle_filter_products(request,context,getProducts)
        return render(request, self.template_name, context)


@csrf_exempt
def getStockProduct(request, slug, id, type):
    context = {}
    product = getProductBySlug(request, slug)
    if type == 'color':
        productStock = ProductStock.objects.filter(product_id=product.id, color_id=id, count__gt=0)
        productStock = Distinct(ProductStock, productStock, 'size_id')
    else:
        productStock = ProductStock.objects.filter(product_id=product.id, size_id=id, count__gt=0)
        productStock = Distinct(ProductStock, productStock, 'color_id')

    result = []
    if ListIsNone(productStock) == False:
        for ps in productStock:
            ps_dict = {
                'productStock_id': ps.id,
                'count': ps.count,
                'color': ps.color.name,
                'color_color': ps.color.color,
                'color_id': ps.color.id,
                'size': ps.size.name,
                'size_id': ps.size.id,
                'size_title': ps.size.title
            }
            result.append(ps_dict)
        context['result'] = result
        context['status'] = '200'
        context['type'] = type
    else:
        context['status'] = '404'
    return JsonResponse(context)


def addProductToCart(request, slug):
    if request.method == 'POST':
        data = request.POST
        product = getProductBySlug(request, slug)
        color = data.get('color')
        size = data.get('size')
        count = data.get('count')
        try:
            count = int(count)
            if int(count) < 1:
                count = 1
            getStockProduct = ProductStock.objects.filter(product_id=product.id, color_id=color, size_id=size).last()
            if getStockProduct != None:
                if request.user.id != None:
                    cart = Cart.objects.filter(user_id=request.user.id).first()
                    if cart == None:
                        cart = Cart.objects.create(user_id=request.user.id)
                else:
                    getCartID = request.COOKIES.get('cartID') or None
                    cart = Cart.objects.filter(cart_id=getCartID).first()
                    if cart == None:
                        cart = Cart.objects.create()

                cartDetail = CartDetail.objects.filter(product_id=product.id,
                                                       productStock_id=getStockProduct.id,cart__id=cart.id).first()
                if cartDetail == None:
                    cartDetail = CartDetail.objects.create(product_id=product.id, productStock_id=getStockProduct.id,
                                                           count=count)
                else:
                    if getStockProduct.count >= cartDetail.count + count:
                        cartDetail.count += count
                    else:
                        cartDetail.count = getStockProduct.count
                    cartDetail.save()
                cart.details.add(cartDetail)
                res = HttpResponseRedirect(resolve_url('user:cart'))
                res = Set_Cookie(res, 'cartID', cart.cart_id)
                return res
        except:
            raise Http404
    raise PermissionDenied()


@csrf_protect
def addProductToWishList(request, slug):
    product = getProductBySlug(request, slug)
    user = request.user
    if user.id != None:
        wishList = WishList.objects.filter(user_id=user.id).first()
        if wishList == None:
            wishList = WishList.objects.create(user_id=user.id)
    else:
        wishlistID = request.COOKIES.get('wishlistID')
        wishList = WishList.objects.filter(wishlist_id=wishlistID).first()
        if wishList == None:
            wishList = WishList.objects.create(user_id=user.id)

    wishDetail = WishDetail.objects.filter(product_id=product.id,wishlist__id=wishList.id).first()
    if wishDetail == None:
        wishDetail = WishDetail.objects.create(product_id=product.id)

    wishList.details.add(wishDetail)
    res = HttpResponseRedirect(resolve_url('product:products'))
    res = Set_Cookie(res, 'wishlistID', wishList.wishlist_id)
    return res



def removeDetailCart(request):
    if request.method == 'POST' and request.is_ajax():
        context = {}
        try:
            data = json.loads(request.body)
            cartID = data.get('cartID') or 0
            detailID = data.get('detailID') or 0
            if request.user.id != None:
                cart = Cart.objects.filter(id=cartID, user_id=request.user.id).first()
            else:
                cart_id = request.COOKIES.get('cartID') or ''
                cart = Cart.objects.filter(id=cartID,cart_id=cart_id).first()
            detail = CartDetail.objects.filter(id=detailID, cart__id=cart.id).first()
            if detail != None:
                detail.delete()
                context['status'] = '200'
                context['newPrice'] = cart.getPrice
                context['newCount'] = cart.getDetailsCount()
            else:
                context['status'] = '404'
        except:
            context['status'] = '404'
        return JsonResponse(context)
    raise PermissionDenied




def removeDetailWish(request):
    if request.method == 'POST' and request.is_ajax():
        context = {}
        try:
            data = json.loads(request.body)
            wishListID = data.get('wishListID') or 0
            wishDetailID = data.get('wishDetailID') or 0
            if request.user.id != None:
                wishList = WishList.objects.filter(id=wishListID,user_id=request.user.id).first()
            else:
                wishList_id = request.COOKIES.get('wishlistID') or ''
                wishList = WishList.objects.filter(id=wishListID,wishlist_id=wishList_id).first()
            wishdetail = WishDetail.objects.filter(id=wishDetailID,wishlist__id=wishList.id).first()
            if wishdetail != None:
                wishdetail.delete()
                context['status'] = '200'
        except:
            context['status'] = '404'
        return JsonResponse(context)
    raise PermissionDenied



def addComment(request,slug):
    if request.method == 'POST':
        user = request.user
        if user.id != None:
            product = getProductBySlug(request,slug)
            data = request.POST
            title = data.get('commentTitle') or None
            message = data.get('commentMessage') or None
            score = int(data.get('commentScore')) or 5
            if title and message and score:
                if score > 5:
                    score = 5
                elif score < 1:
                    score = 1
                Comment.objects.create(user_id=user.id,product_id=product.id,title=title,message=message,score=score)
                return Set_Cookie_Functionality('Your comment was successfully submitted','Success') # Show Message
            else:
                return Set_Cookie_Functionality('Please fill fields comment','Error')
    raise PermissionDenied()



def checkCoupon(request):
    if request.method == 'POST' and request.is_ajax():
        context = {}
        data = json.loads(request.body)
        code = data.get('code') or ''
        coupon = Coupon.objects.filter(code=code).first()
        orderID = data.get('orderID')
        order = Order.objects.filter(id=orderID).first()
        cartID = data.get('cartID')
        cart = Cart.objects.filter(id=cartID).first()
        if order != None and cart != None and order.withCoupon == False:
            if coupon != None and coupon.count > 0 and coupon.price < order.getPrice():
                price = float(order.shipping.price) + float(cart.getPrice)
                totalPrice = coupon.getPrice(price)
                order.withCoupon = True
                order.couponPrice = coupon.price
                order.coupon = coupon
                order.save()
                coupon.count -= 1
                coupon.save()
                context['price'] = totalPrice
                context['status'] = '200'
            else:
                context['status'] = '404'
            return JsonResponse(context)
    raise PermissionDenied