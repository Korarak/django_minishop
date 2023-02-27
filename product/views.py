from django.shortcuts import render,redirect
from django.contrib import messages
from datetime import datetime
from .models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q

# Create your views here.
def del_cart_item(request,id):
    user = request.user
    item_del = cart_add.objects.get(product_id_id=id,email=user.email)
    item_del.delete()
    return redirect("/cart")

def showMyorder(request):
    user = request.user
    order_show_detail = []
    myorder_count = order_data.objects.filter(order_email=user.email).count()
    if myorder_count > 0:
        if user.is_staff == 0:
            myorder = order_data.objects.filter(order_email=user.email)
            detail = order_detail.objects.all()
            context = {'showmyorder' : myorder , 'dtl' : detail}
            return render(request,'productapp/myorder.html',context)
        else :
            myorder = order_data.objects.all()
            detail = order_detail.objects.all()
            context = {'showmyorder' : myorder , 'dtl' : detail}
            return render(request,'productapp/myorder.html',context)
    else:
        return render(request,'productapp/myorder.html')

def checkout(request):
    user = request.user
    sum_order = cart_add.objects.filter(email=user.email)
    Nowtime = datetime.now()
    total = []
    if sum_order.count() <= 0:
        return redirect("/")
    else:    
        for item in sum_order:
            """ print(item.product_price)
            print(item.product_qty) """
            sum_item = float(item.product_price) * float(item.product_qty)
            total.append(sum_item)
        total_order = (sum(total))
        print(sum_order)
    if request.method == 'POST':
            checkout = order_detail()
            save_order = order_data()
            save_order.order_total = total_order
            save_order.order_date = Nowtime
            save_order.order_address = request.POST.get('order_address')
            save_order.order_tel = request.POST.get('order_tel')
            save_order.order_username = user.username
            save_order.order_email = user.email
            save_order.save()
            for x in sum_order:
                save_order_id = order_data.objects.filter(order_email=user.email).last()
                checkout = order_detail()
                checkout.order_id_ref_id =  int(save_order_id.order_id)
                checkout.p_id = x.product_id
                checkout.p_qty = x.product_qty
                checkout.p_price = x.product_price
                print(checkout.p_id)
                print(checkout.p_qty)
                print(checkout.p_price)
                checkout.save()
                del_cart = cart_add.objects.get(product_id_id= checkout.p_id,email=user.email)
                del_cart.delete()
            messages.success(request,'สำเร็จ')
            return redirect('/showMyorder')
    showcart = {'item' : cart_add.objects.filter(email=user.email) , 
                'total_order' : total_order,
                'nowtime' : Nowtime,
                }
    return render(request,'productapp/checkout.html',showcart)

def addtocart(request,id):
    user = request.user
    if request.user.is_authenticated :
        if user.email == '':
            messages.warning(request, 'กรุณาเพิ่ม e-mail')
            return redirect('/myprofile')
        else:
                add_product = product_data.objects.get(pk=id)
                table = cart_add()
                if cart_add.objects.filter(product_id_id=id,email=user.email):
                    if cart_add.objects.filter(product_id_id=id,email=user.email) is not None:
                        increase_qty = cart_add.objects.get(product_id_id=id,email=user.email)
                        increase_qty.product_qty = increase_qty.product_qty + 1
                        increase_qty.save()
                        return redirect('/cart')  
                else:
                    table.product_id_id = add_product.product_id
                    table.product_qty = 1
                    table.product_price = int(add_product.product_price)
                    table.email = user.email
                    table.save()
                    return redirect('/cart')
    else:
        messages.warning(request,'เข้าสู่ระบบเพื่อสั่งสินค้า')
        return redirect('/login')

def cart(request):
    user = request.user
    showcart = {'item' : cart_add.objects.filter(email=user.email)}
    return render(request,'productapp/cart.html',showcart)

def search(request):
    if request.method == 'POST':
        if request.POST.get('search_product'):
            print(request.POST.get('search_product'))
            s_product = request.POST.get('search_product')
            context = {'result' : product_data.objects.filter(product_name__startswith=s_product)}
            return render(request,'productapp/search.html',context)
        else:
            context = {'result' : product_data.objects.all()}
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

def editprofile(request,id):
    if request.method == "POST":
        if request.POST.get('username'):
            print(request.POST.get('username'))
            print(request.POST.get('firstname'))
            print(request.POST.get('lastname'))
            print(request.POST.get('email'))
            table = User.objects.get(pk=id)
            table.username = request.POST.get('username')
            table.first_name = request.POST.get('firstname')
            table.last_name = request.POST.get('lastname')
            table.email = request.POST.get('email')
            table.save()
            messages.success(request,'แก้ไขข้อมูลสำเร็จ')
            return redirect('/myprofile')
    return render(request,'productapp/editprofile.html')

def editproduct(request,id):
    context = {'product': product_data.objects.get(pk=id)}
    if request.method == "POST":
        print(request.POST.get('product_name'))
        print(request.POST.get('product_qty'))
        print(request.POST.get('product_price'))
        print(request.POST.get('product_detail'))
        table = product_data.objects.get(pk=id)
        table.product_name = request.POST.get('product_name')
        table.product_qty = request.POST.get('product_qty')
        table.product_price = request.POST.get('product_price')
        table.product_detail = request.POST.get('product_detail')
        table.save()
        messages.success(request,'แก้ไขข้อมูลสำเร็จ')
        return redirect('/product')
    else:
        return render(request,'productapp/editproduct.html', context)

def confirm_productdel(request,id):
    order = order_detail.objects.filter(p_id=id)
    cart = cart_add.objects.filter(product_id=id)
    if order.count() > 0 or cart.count() > 0:
        context = {'status_del': False, 'product' : product_data.objects.get(pk=id)}
    else:
        context = {'status_del': True, 'product' : product_data.objects.get(pk=id)}
    return render(request,'productapp/product_del.html', context)

def product_del(request,id):
    item_del = product_data.objects.get(pk=id)
    item_del.delete()
    return redirect("/product")

def product(request):
    context = {'product' : product_data.objects.all()}
    return render(request,'productapp/product.html',context)

def orders(request):
    context = {'orders' : order_data.objects.all(), 'dtl' : order_detail.objects.all()}
    return render(request,'productapp/orders.html',context)

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
            return redirect('/product')
    return render(request,'productapp/addproduct.html')

def admin_custom(request):
    return render(request,'productapp/admin_custom.html')