from django.shortcuts import render,redirect
from django.contrib import messages
from datetime import datetime
from .models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def addtocart(request,id):
    user = request.user
    add_product = product_data.objects.get(pk=id)
    table = cart_add()
    table.product_id = add_product.product_id
    table.product_qty = 1
    table.product_price = int(add_product.product_price)
    table.email = user.email
    table.save()
    return redirect('/cart')

def cart(request):
    return render(request,'productapp/cart.html')

def search(request):
    if request.method == 'POST':
        if request.POST.get('search_product'):
            print(request.POST.get('search_product'))
            s_product = request.POST.get('search_product')
            context = {'result' : product_data.objects.filter(product_name__startswith=s_product)}
            return render(request,'productapp/search.html',context)
    return render(request,'productapp/search.html')

def showproduct(request):
    context = {'product' : product_data.objects.all()}
    return render(request,'productapp/showproduct.html',context)

def base(request):
    return render(request,'productapp/base.html')

def login(request):
    if request.method == 'POST':
        if request.POST.get('uname'):
            chkuname = request.POST.get('uname')
            chkpw = request.POST.get('pwd')
            print(chkuname)
            print(chkpw)
            user = auth.authenticate(request,username=chkuname,password=chkpw)
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(86400) #ตั้งเวลาถอยหลังให้หมด session
                    auth.login(request, user) #เมื่อ login สำเร็จให้ส่งค่า user ไปที่หน้า tempates html
                    messages.success(request,'เข้าสู่ระบบสำเร็จ')
                    return redirect('/')
            else:
                messages.warning(request,"ไม่ถูกต้อง ลองใหม่")
                return redirect('/login')
    return render(request,"productapp/login.html")

def register(request):
    if request.method=="POST":
        username=request.POST['uname']       
        pass1=request.POST['pwd1']
        pass2=request.POST['pwd2']
        #รับค่าจาก form register.html
        if pass1==pass2: #ตรวจสอบ password ตรงกันหรือไม่
            if User.objects.filter(username=username).exists(): #ถ้า username เกิดซ้ำ
                messages.warning(request,'OOPS! Usename already taken')
                return redirect('/register')            
            else:
                user=User.objects.create_user(username=username,password=pass1)
                user.save() #ถ้า username ไม่ซ้ำ ให้บันทึกลง database
                #ตรวจสอบที่ตาราง auth_user
                messages.success(request,'Account created successfully!!')
                return redirect('/login')
        else:
            messages.warning(request,'Password do not match') #เตือนว่า password ไม่ตรงกัน
            return redirect('/register')
    return render(request,'productapp/register.html')

def logout(request):
    # Log user out
    auth.logout(request)
    return redirect('/login')
    return render(request,'productapp/login.html')

def myprofile(request):
    return render(request,'productapp/myprofile.html')

def editproduct(request):
    context = {'product' : product_data.objects.all()}
    return render(request,'productapp/editproduct.html',context)

def addproduct(request):
    if request.method == "POST":
        if request.POST.get("product_name"):
            table = product_data()
            table.product_name = request.POST.get('product_name')
            table.product_qty = request.POST.get('product_qty')
            table.product_price = request.POST.get('product_price')
            table.product_detail = request.POST.get('product_detail')
            table.save()
            messages.success(request,'เพิ่มข้อมูลสำเร็จ')
            return redirect('/editproduct')
    return render(request,'productapp/addproduct.html')