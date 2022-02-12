from django.shortcuts import render
from django.views.generic import View
from User.models import User
from django.db.models import Value, Max, F, Case, When, Sum
from Product.models import Product, Category, Brand, Color


class products(View):
    template_name = 'Products/index.html'

    def get(self, request, *args, **kwargs):
        context = {}

        getProducts = Product.getProducts.all()
        # Filter Products
        getCategories = Category.objects.all()
        getBrands = Brand.objects.all()
        getColors = Color.objects.all()

        highsetPriceProduct = getProducts.aggregate(highsetPrice=Max('price'))['highsetPrice']
        rangePriceFilter = f'0-{highsetPriceProduct}'

        filterIsActive = request.GET.get('filter') or False

        def getListValueFilter(strList):
            # list with string => [name-1,name-2] => number is pk
            if strList:
                try:
                    strList = eval(strList)
                    if type(strList) == list:
                        strList = [i.split('-')[-1] for i in strList]
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
                    priceEnd = filter_range.split('-')[-1]
                except:
                    priceStart = 0
                    priceEnd = highsetPriceProduct
            else:
                priceStart = 0
                priceEnd = highsetPriceProduct
            rangePriceFilter = f"{priceStart}-{priceEnd}"
            # Filter products
            getProducts = getProducts.filter(categories__in=filter_categories, colors__in=filter_colors,
                                             brand__in=filter_brands, price__gte=priceStart, price__lte=priceEnd)

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

        # Response
        context['highsetPriceProduct'] = highsetPriceProduct
        context['rangePriceFilter'] = rangePriceFilter
        context['products'] = getProducts
        context['categories'] = getCategories
        context['brands'] = getBrands
        context['colors'] = getColors
        context['products'] = getProducts.distinct()

        return render(request, self.template_name, context)
