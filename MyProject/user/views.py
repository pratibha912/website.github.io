from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.db import connection
# Create your views here.
def home(req):

    cdata=category.objects.all().order_by('-id')[0:6]
    pdata=products.objects.all().order_by('-id')[0:12]
    #print(pdata)
    noofitemsincart=addtocart.objects.all().count()
    return render(req,'user/index.html',{"data":cdata,"product":pdata,"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

def about(req):
    noofitemsincart = addtocart.objects.all().count()
    return render(req,'user/about.html',{"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

def contactus(request):
    status=False
    if request.method=='POST':
         Name=request.POST.get("name","")
         Mobile=request.POST.get("mobile","")
         Email=request.POST.get("email","")
         Message=request.POST.get("msg","")
         x=contact(name=Name,mobile=Mobile,email=Email,message=Message)
         x.save()
         status=True
         # return HttpResponse("<script>alert('Thanks for enquiry..');window.location.href='/user/contactus/'</script>")
    noofitemsincart = addtocart.objects.all().count()
    return render(request,'user/contactus.html',{'S':status,"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

def services(req):
    return render(req,'user/services.html')

def myorders(request):
    userid=request.session.get('user')
    oid=request.GET.get('oid')
    orderdata=""
    if userid:
        cursor=connection.cursor()
        cursor.execute("select o.*,p.* from user_order o,user_products p where o.id=p.id and o.userid='"+str(userid)+"'")
        orderdata=cursor.fetchall()
        if oid:
             result=order.objects.filter(id=oid,userid=userid)
             result.delete()
             return HttpResponse("<script>alert('Your order has been cancelled..');window.location.href='/user/myorders/'</script>")
    noofitemsincart = addtocart.objects.all().count()
    return render(request,'user/myorders.html',{"pendingorder":orderdata,"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

def myprofile(request):
    user=request.session.get('user')
    pdata=profile.objects.filter(email=user)
    if user:
        #d = profile.objects.filter(email=email)
        if request.method == 'POST':
            name = request.POST.get("name", "")
            mobile = request.POST.get("mobile", "")
            #email = request.POST.get("email", "")
            password = request.POST.get("passwd", "")
            gender = request.POST.get("gender", "")
            address = request.POST.get("address", "")
            picname = request.FILES['fu']

            profile(email=user,name=name,passwd=password,mobile=mobile,ppic=picname,address=address,gender=gender).save()
            return HttpResponse("<script>alert('Your profile updated successfully..');window.location.href='/user/myprofile/'</script>")
    noofitemsincart = addtocart.objects.all().count()
    return render(request,'user/myprofile.html',{"profile":pdata,"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

def prod(request):
    cdata=category.objects.all().order_by('-id')
    x=request.GET.get('abc')
    if x is not None:
        pdata=products.objects.filter(category=x)
    else:
        pdata = products.objects.all().order_by('-id')
    noofitemsincart = addtocart.objects.all().count()
    return render(request,'user/product.html',{"cat":cdata,"product":pdata,"noofitemsincart":noofitemsincart})
    print(noofitemsincart)


def signup(request):
    if request.method=='POST':
        name=request.POST.get("name","")
        mobile=request.POST.get("mobile", "")
        email=request.POST.get("email", "")
        password=request.POST.get("passwd", "")
        gender=request.POST.get("gender","")
        address=request.POST.get("address", "")
        picname=request.FILES['fu']
        d=profile.objects.filter(email=email)

        if d.count()>0:
            return HttpResponse("<script>alert('You are already registerd..');window.location.href='/user/signup/'</script>")
        else:
            res=profile(name=name,mobile=mobile,email=email,passwd=password,gender=gender,address=address,ppic=picname)
            res.save()
            return HttpResponse("<script>alert('You are registerd successfully..');window.location.href='/user/signup/'</script>")
    noofitemsincart = addtocart.objects.all().count()
    return render(request,'user/signup.html',{"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

def signin(request):
    if request.method=="POST":
        email=request.POST.get('email')
        passwd=request.POST.get('password')
        data=profile.objects.filter(email=email,passwd=passwd)
        if data.count()>0:
            request.session["user"]=email
            return HttpResponse("<script>alert('Thanks for login');window.location.href='/user/signin';</script>")
        else:
            return HttpResponse("<script>alert('Your Email or Password are incorrect..');window.location.href='/user/signin';</script>")
    noofitemsincart = addtocart.objects.all().count()
    return render(request,'user/signin.html',{"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

def logout(request):
    del request.session['user']
    return HttpResponse("<script>window.location.href='/user/home/'</script>")


def viewdetails(request):
     a=request.GET.get('msg')
     data=products.objects.filter(id=a)
     noofitemsincart = addtocart.objects.all().count()
     return render(request,'user/viewdetails.html',{"d":data,"noofitemsincart":noofitemsincart})
     print(noofitemsincart)

def process(request):
    userid=request.session.get('user')
    pid=request.GET.get('pid')
    btn=request.GET.get('bn')
    print(userid,pid,btn)
    if userid is not None:
        if btn=='cart':
             checkcartitem=addtocart.objects.filter(pid=pid,userid=userid)
             if checkcartitem.count()==0:
                 addtocart(pid=pid,userid=userid,status=True,cdate=datetime.datetime.now()).save()
                 return HttpResponse("<script>alert('Your item is successfully added in cart..');window.location.href='/user/home/'</script>")

             else:
                 return HttpResponse("<script>alert('This item is alerady added in cart...');window.location.href='/user/home/'</script>")
        elif btn=='order':
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('Your order have confirmed...');window.location.href='/user/myorders/'</script>")

        elif btn=='orderfromcart':
            res=addtocart.objects.filter(pid=pid,userid=userid)
            res.delete()
            order(pid=pid,userid=userid,remarks="Pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('Your order have confirmed...');window.location.href='/user/myorders/'</script>")

        return render(request, 'user/process.html', {"alreadylogin": True})
    else:
        return HttpResponse("<script>window.location.href='/user/signin/'</script>")





def cart(request):
    if request.session.get('user'):
        userid=request.session.get('user')
        cursor=connection.cursor()
        cursor.execute("select c.*,p.* from user_addtocart c,user_products p where p.id=c.pid and userid='"+str(userid)+"'")
        cartdata=cursor.fetchall()
        pid=request.GET.get('pid')
        if request.GET.get('pid'):
            res=addtocart.objects.filter(id=pid,userid=userid)
            res.delete()
            return HttpResponse("<script>alert('Your product has been removed successfully');window.location.href='/user/cart/'</script>")
    noofitemsincart = addtocart.objects.all().count()
    return render(request,'user/cart.html',{"cart":cartdata,"noofitemsincart":noofitemsincart})
    print(noofitemsincart)

