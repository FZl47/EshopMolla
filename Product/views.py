from django.shortcuts import render , Http404
from django.views.generic import View
from User.models import User
from django.db.models import Value, Max, F, Case, When, Sum , Q
from Product.models import Product, Category, Brand, Color , orderByPopulariy , orderByDate , orderByPrice
from django.core.paginator import Paginator
from django.db import connection , reset_queries
import math




def getProductPagination(req,listProducts):
    step = 3 # How many products to display
    def noneVal():
        pagination = Paginator([], step)
        pagination.currentPage = 1
        pagination.step = step
        return [], pagination.get_page(1), pagination
    numberPage = req.GET.get('page') or 1
    pagination = Paginator(listProducts,step)
    try:
        numberPage = int(numberPage)
        if numberPage < 1 :
            numberPage = 1
        pagination.currentPage = numberPage
        pagination.step = step
        pagination.countPages = int(math.ceil((len(listProducts) / step)))
        pagination.lastPage = pagination.countPages
        listRange = []
        if numberPage - 1 > 1:
            listRange.append(numberPage-1)
        for i in range(numberPage,numberPage+3):
            if i < pagination.lastPage and i > 1:
                listRange.append(i)
        pagination.listRange = listRange
    except:
        return noneVal()
    if numberPage <= pagination.num_pages:
        getPage = pagination.get_page(numberPage)
        return getPage.object_list , getPage , pagination
    return noneVal()


class products(View):
    template_name = 'Products/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        getProducts = Product.getProducts.select_related('brand').prefetch_related('categories').all()

        # Search Products
        searchIsActive = request.GET.get('search') or False
        if searchIsActive:
            context['searchIsActive'] = True
            context['searchContent'] = searchIsActive
            if str(searchIsActive).isdigit():
                lookUp = Q(title__icontains=searchIsActive) | Q(price=searchIsActive) | Q(categories__title__icontains=searchIsActive)
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
                getProducts = getProducts.filter(categories__in=filter_categories, stockProduct__color__in=filter_colors,colors__count__gt=0,
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

        #Order
        #By default ordered by popularity
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
        resultProducts , pageActive, pagination = getProductPagination(request, getProducts)

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
        return render(request, self.template_name, context)



class product(View):
    template_name = 'Product/index.html'

    def get(self,request,slug):
        return render(request,self.template_name)