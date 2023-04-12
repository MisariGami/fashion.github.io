from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Banner, Category, Brand, Product, ProductAttribute, CartOrder, CartOrderItems, Wishlist
from django.template.loader import render_to_string
from .forms import SignupForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Home Page
def home(request):
    banners = Banner.objects.all().order_by("-id")
    data = Product.objects.filter(is_featured=True).order_by("-id")
    return render(request, "index.html", {"data": data, "banners": banners})

# Category
def category_list(request):
    data = Category.objects.all().order_by("-id")
    return render(request, "category_list.html", {"data": data})

# Brand
def brand_list(request):
    data = Brand.objects.all().order_by("-id")
    return render(request, "brand_list.html", {"data": data})

# Product List
def product_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by("-id")
    cats = Product.objects.distinct().values("category__title", "category__id")
    brands = Product.objects.distinct().values("brand__title", "brand__id")
    colors = Product.objects.distinct().values(
        "color__title", "color__id", "color__color_code"
    )
    sizes = Product.objects.distinct().values("size__title", "size__id")
    return render(
        request,
        "product_list.html",
        {
            "data": data,
            "total_data": total_data,
            "cats": cats,
            "brands": brands,
            "colors": colors,
            "sizes": sizes,
        },
    )

# Product List According to Category
def category_product_list(request, cat_id):
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by("-id")
    cats = Product.objects.distinct().values("category__title", "category__id")
    brands = Product.objects.distinct().values("brand__title", "brand__id")
    colors = Product.objects.distinct().values(
        "color__title", "color__id", "color__color_code"
    )
    sizes = Product.objects.distinct().values("size__title", "size__id")
    return render(
        request,
        "category_product_list.html",
        {
            "data": data,
            "cats": cats,
            "brands": brands,
            "colors": colors,
            "sizes": sizes,
        },
    )

# Product List According to Brand
def brand_product_list(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by("-id")
    cats = Product.objects.distinct().values("category__title", "category__id")
    brands = Product.objects.distinct().values("brand__title", "brand__id")
    colors = Product.objects.distinct().values(
        "color__title", "color__id", "color__color_code"
    )
    sizes = Product.objects.distinct().values("size__title", "size__id")

    return render(
        request,
        "category_product_list.html",
        {
            "data": data,
            "cats": cats,
            "brands": brands,
            "colors": colors,
            "sizes": sizes,
        },
    )

# Product Detail
def product_detail(request, slug, id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[
        :4
    ]
    colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
    return render(
        request,
        "product_detail.html",
        {
            "data": product,
            "related": related_products,
            "colors":colors,
            "sizes":sizes,
        },
    )

# Search
def search(request):
    q = request.GET["q"]
    data = Product.objects.filter(title__icontains=q).order_by("-id")
    return render(request, "search.html", {"data": data})

# Filter Data
def filter_data(request):
    colors = request.GET.getlist("color[]")
    categories = request.GET.getlist("category[]")
    brands = request.GET.getlist("brand[]")
    sizes = request.GET.getlist("size[]")
    allProducts = Product.objects.all().order_by("-id").distinct()
    if len(colors) > 0:
        allProducts = allProducts.filter(
            productattribute__color__id__in=colors
        ).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(
            productattribute__size__id__in=sizes
        ).distinct()
    t = render_to_string("ajax/product-list.html", {"data": allProducts})
    return JsonResponse({"data": t})

#add to cart
def add_to_cart(request):
    cart_p={}
    cart_p[str(request.GET['id'])]={
        'image':request.GET['image'],
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p

    return JsonResponse({'data': request.session['cartdata'], 'totalitems':len(request.session['cartdata'])})

#cart list page
def cart_list(request):
    total_amt=0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems':len(request.session['cartdata']), 'total_amt':total_amt})
    else:
        return render(request, 'cart.html', {'cart_data':'','totalitems':0,'total_amt':total_amt})

#delete from cart
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


#update cart
def update_cart_item(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']= cart_data
    
    total_amt=0
    for p_id, item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    t=render_to_string('ajax/cart-list.html',{'cart_data': request.session['cartdata'], 'totalitems':len(request.session['cartdata']), 'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

#signup
def signup(request):
    form=SignupForm()
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=pwd)
            login(request,user)
            return redirect('home')
    
    return render(request, 'registration/signup.html', {'form':form})

# checkout
@login_required
def checkout(request):
    totalAmt=0
    total_amt=0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt+=int(item['qty'])*float(item['price'])
        # Order
        order=CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt
        )

        for p_id, item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        # OrderItems
        items=CartOrderItems.objects.create(
            order=order,
            invoice_no='INV-'+str(order.id),
            item=item['title'],
            image=item['image'],
            qty=item['qty'],
            price=item['price'],
            total=float(item['qty'])*float(item['price'])
        )

#user dashboard

import calendar
def my_dashboard(request):
	# orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
	# monthNumber=[]
	# totalOrders=[]
	# for d in orders:
	# 	monthNumber.append(calendar.month_name[d['month']])
	# 	totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html')

# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)


# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/wishlist.html',{'wlist':wlist})
