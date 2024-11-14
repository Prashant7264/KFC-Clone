from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from kfcstoreapp.models import product,cart, Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def main(request):
    #userid=request.user.id
    #uname=request.user.username
    #print(userid)
    #context={}
    #p=product.objects.filter(is_active=True)
    #context['products']=p
    return render(request,'main.html')

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cannot be empty!!"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/main')
            else:
                context['errmsg']="Invalid Username/password!!"
                return render(request,'login.html',context)

    else:
         return render(request,'login.html')

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields cannot be empty!!"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Password is not matching!!"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['successmsg']="User Registered successfully!!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already Exit's, try log in!!"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def ulogout(request):
    logout(request)
    return redirect('/main')

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        print(u[0])
        p=product.objects.filter(id=pid)
        print(p)
        print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=cart.objects.filter(q1 & q2)
        print(len(c))
        context={}
        context["products"]=p
        n=len(c)
        if n==1:
            context["errmsg"]=" Product is already added to cart!!"
        else:
            c=cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context["success"]=" Product Added to cart Successfully!!"
        return render(request,'order.html',context)
    else:
        return redirect("/login")

def viewcart(request):
    c=cart.objects.filter(uid=request.user.id)
    #print(c)
    #print(c[0])
    #print(c[0].uid)
    #print(c[0].pid)
    #print(c[0].pid.name)
    #print(c[0].pid.price)
    s=0
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    print(s)
    context={}
    context['data']=c
    context['total']=s
    return render(request,'viewcart.html',context)

def updateqty(request,qv,cid):
    c=cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart")

def remove(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def range_filter(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price range
    products = product.objects.all()
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {'products': products, 'min_price': min_price, 'max_price': max_price}
    return render(request, 'deal.html', context)

def deal(request):
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'deal.html',context)

def contact(request):
    return render(request,'contact.html')

def order(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'order.html',context)

def placeorder(request):
    userid=request.user.id
    c=cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete() 
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    context['total']=s 
     
    return render(request,"placeorder.html",context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    np=len(orders)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_wIRW5UcLnuojt3", "TAWQaJo7pF8PxWMwC5MwnOQg"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    
    return render(request,'pay.html')

def sendusermail(request):
    try:
        send_mail(
        "Order Placed!!",
        "Estore-order Placed Successfully!.",
        "prashantgadale250@gmail.com",
        ["prashantgadale2001@gmail.com"],
        fail_silently=False,
        )
        return HttpResponse("mail sent!!")
    except Exception:
        return HttpResponse("mail sent!!")
    
def search(request):
    query = request.GET.get('query')  
    context = {}
    if query:
        products = product.objects.filter(name__icontains=query)  
        context['products'] = products
        context['query'] = query
    else:
        products = product.objects.all()
        context['products'] = products

    return render(request, 'deal.html', context)