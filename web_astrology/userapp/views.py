from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from accounts.models import *
from django.contrib import messages
from datetime import datetime
from adminapp.models import *
from userapp.models import *
from datetime import datetime
import razorpay
# Create your views here.
import requests
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail


def HomePage(request):
    bloglist = DailyBlogs.objects.all()[:3]
    try:
        horoscopecat = HoroscopeCategory.objects.all() 
        puja = Pooja.objects.all()    
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        return render(request, 'index.html', {'mypuja':puja, 'horoscop':horoscopecat, 'lst':bloglist,'cart':count_cart,'pooja':count_puja})
    except:
        
        return render(request, 'index.html', {'lst':bloglist})


def FilterHoroscopeByCategory(request,id):
    # catname = HoroscopeCategory.objects.all()
    cateid  = HoroscopeCategory.objects.get(id=id)
    print("category ", cateid)
    catfilter = Horoscope.objects.filter(horscopname=cateid)
    print("My category",catfilter)
    return render(request, "horoscope_single.html", {'catid':cateid, 'catfilter':catfilter})






# Show all Pooja with category
def OurServices(request):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        catname = CategoryOfPooja.objects.all()
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        pojadetail = Pooja.objects.all()
        catfilter1=[]
        for i in pojadetail:
             if i.category.active_status:
                 if i.active_status:
                    catfilter1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catfilter1)
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Pooja.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        
        mylist = zip(catname1, lst)
        
        if 'q' in request.GET:
            q = request.GET['q']
            # data = Data.objects.filter(last_name__icontains=q)
            multiple_q = Q(Q(name__contains=q) | Q(discription__contains=q) | Q(advantages__contains=q) | Q(category__catname__contains=q) | Q(price__contains=q))
            data = Pooja.objects.filter(multiple_q)
            
            # print("ewfweewdfewew  :fwfw", data[0].email)
            context = {
                'data': data,
                'cart':count_cart,
                'pooja':count_puja,
                'mylist':mylist
            }
            return render(request, "search-puja.html",context)
        
        paginator = Paginator(catfilter1, 6)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        totalpage = all_lead.paginator.num_pages
        
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'catname':catname1, 
            'puja':catfilter1,
            'cart':count_cart,
            'pooja':count_puja,
            'mylist':mylist
        }
        return render(request, 'service_single.html', context)
    except:
        catname = CategoryOfPooja.objects.all()
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        pojadetail = Pooja.objects.all()
        catfilter1=[]
        for i in pojadetail:
             if i.category.active_status:
                 if i.active_status:
                    catfilter1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catfilter1)
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Pooja.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        
        mylist = zip(catname1, lst)
        
        if 'q' in request.GET:
            q = request.GET['q']
            # data = Data.objects.filter(last_name__icontains=q)
            multiple_q = Q(Q(name__contains=q) | Q(discription__contains=q) | Q(advantages__contains=q) | Q(category__catname__contains=q) | Q(price__contains=q))
            data = Pooja.objects.filter(multiple_q)
            
            # print("ewfweewdfewew  :fwfw", data[0].email)
            context = {
                'data': data,
                'mylist':mylist
            }
            return render(request, "search-puja.html",context)
        
        paginator = Paginator(catfilter1, 6)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        totalpage = all_lead.paginator.num_pages
        
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'catname':catname1, 
            'puja':catfilter1,
            'mylist':mylist
        }
        return render(request, 'service_single.html', context)
        
# Filter Pooja By category
def FilterByCategory(request,id):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        catname = CategoryOfPooja.objects.all()
        cateid  = CategoryOfPooja.objects.get(id=id)
        print(cateid)
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        catfilter = Pooja.objects.filter(category=cateid)
        catfilter1=[]
        for i in catfilter:
             if i.category.active_status:
                 if i.active_status:
                    catfilter1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catfilter1)
        print("My category",catfilter)
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Pooja.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        
        mylist = zip(catname1, lst)
        return render(request, "service_single.html", {'catid':cateid, 'catfilter':catfilter1, 'catname':catname1,'cart':count_cart,'pooja':count_puja,'mylist':mylist})
    except:
        catname = CategoryOfPooja.objects.all()
        cateid  = CategoryOfPooja.objects.get(id=id)
        print(cateid)
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        catfilter = Pooja.objects.filter(category=cateid)
        catfilter1=[]
        for i in catfilter:
             if i.category.active_status:
                 if i.active_status:
                    catfilter1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catfilter1)
        print("My category",catfilter)
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Pooja.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        
        mylist = zip(catname1, lst)
        return render(request, "service_single.html", {'catid':cateid, 'catfilter':catfilter1, 'catname':catname1,'mylist':mylist})
        
        
        
        
        
# Show all Product with category
def OurProducts(request):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        catname = CategoryOfProduct.objects.all()
        
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        proddetail = Products.objects.all()
        proddetail1=[]
        for i in proddetail:
             if i.category.active_status:
                 if i.active_status:
                    proddetail1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',proddetail1)
        
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Products.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        
        mylist = zip(catname1, lst)
        
        
        if 'q' in request.GET:
            q = request.GET['q']
            # data = Data.objects.filter(last_name__icontains=q)
            multiple_q = Q(Q(prodname__contains=q) | Q(discription__contains=q) | Q(price__contains=q) | Q(category__catprod__contains=q) | Q(offers__contains=q))
            data = Products.objects.filter(multiple_q)
            
            # print("ewfweewdfewew  :fwfw", data[0].email)
            context = {
                'data': data,
                'cart':count_cart,
                'pooja':count_puja,
                'mylist':mylist
            }
            return render(request, "search-product.html",context)
        
        paginator = Paginator(proddetail1, 6)
        print(paginator)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        print(">>>>>>>>",all_lead)
        totalpage = all_lead.paginator.num_pages
        # for i in all_lead:
        #     print(i)
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'catname':catname1, 
            'product':proddetail1,
            'cart':count_cart,
            'pooja':count_puja,
            'mylist':mylist
        }
        return render(request, 'product.html', context)
    except:
        catname = CategoryOfProduct.objects.all()
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        proddetail = Products.objects.all()
        proddetail1=[]
        for i in proddetail:
             if i.category.active_status:
                 if i.active_status:
                    proddetail1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',proddetail1)
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Products.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        
        mylist = zip(catname1, lst)
        
        if 'q' in request.GET:
            q = request.GET['q']
            # data = Data.objects.filter(last_name__icontains=q)
            multiple_q = Q(Q(prodname__contains=q) | Q(discription__contains=q) | Q(price__contains=q) | Q(category__catprod__contains=q) | Q(offers__contains=q))
            data = Products.objects.filter(multiple_q)
            
            # print("ewfweewdfewew  :fwfw", data[0].email)
            context = {
                'data': data,
                
                'mylist':mylist
            }
            return render(request, "search-product.html",context)
        
        paginator = Paginator(proddetail1, 6)
        print(paginator)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        print(">>>>>>>>",all_lead)
        totalpage = all_lead.paginator.num_pages
        # for i in all_lead:
        #     print(i)
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'catname':catname1, 
            'product':proddetail1,
            'mylist':mylist
        }
        return render(request, 'product.html', context)
# Filter Product By category
def FilterProductByCategory(request,id):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        
        catname = CategoryOfProduct.objects.all()
        # prodnm = Products.objects.all()
        cateid  = CategoryOfProduct.objects.get(id=id)
        print(cateid)
        catfilter = Products.objects.filter(category=cateid)
        for i in catfilter:
            print(i.prodname)
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        catfilter1=[]
        for i in catfilter:
             if i.category.active_status:
                 if i.active_status:
                    catfilter1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catfilter1)
        print("My category",catfilter)
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Products.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        mylist = zip(catname1, lst)
        return render(request, "product.html", {'catid':cateid, 'catfilter':catfilter1, 'catname':catname1,'cart':count_cart,'pooja':count_puja,'mylist':mylist})
    except:
        catname = CategoryOfProduct.objects.all()
        # prodnm = Products.objects.all()
        cateid  = CategoryOfProduct.objects.get(id=id)
        print(cateid)
        catfilter = Products.objects.filter(category=cateid)
        for i in catfilter:
            print(i.prodname)
        catname1=[]
        for i in catname:
             if i.active_status:
                 catname1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catname1)
        catfilter1=[]
        for i in catfilter:
             if i.category.active_status:
                 if i.active_status:
                    catfilter1.append(i)
             else:
                 continue
        print('dskfmnaSKdfmadfm',catfilter1)
        print("My category",catfilter)
        lst = []
        for lr in catname:
            # for rl in prodnm:
                procat = Products.objects.filter(category=lr.id).count()
                lst.append(procat)
        print('wsdssssssdfdfdfgrtgrrrhthhr', lst)
        mylist = zip(catname1, lst)
        return render(request, "product.html", {'catid':cateid, 'catfilter':catfilter1, 'catname':catname1,'mylist':mylist})

def ViewProductDetail(request,id):
    try:
        # current_user = User.objects.get(username=request.user)
        # count_cart = Cart.objects.filter(user_id=current_user.id).count()
        # count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        # prod = Products.objects.get(id=id)
        # print(prod)
        # return render(request, "productdetail.html", {'detailprod':prod,'cart':count_cart,'pooja':count_puja})
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        prod = Products.objects.get(id=id)
        print(prod.price)
        print(prod.offers)
        caloffer=(float(prod.price)*float(prod.offers))/100
        cal=float(prod.price)-caloffer
        prodquan=int(prod.quantity)
        ob = Products.objects.filter(id=id)
        ob.update(offerprice=cal)
        return render(request, "productdetail.html", {'detailprod':prod,'cart':count_cart,'pooja':count_puja,'cal':cal, 'prodquan':prodquan})
    except User.DoesNotExist:
        prod = Products.objects.get(id=id)
        print(prod)
        print(prod.price)
        print(prod.offers)
        caloffer=(float(prod.price)*float(prod.offers))/100
        cal=float(prod.price)-caloffer
        prodquan=int(prod.quantity)
        return render(request, "productdetail.html", {'detailprod':prod,'cal':cal, 'prodquan':prodquan})


# def ViewPujaDetail(request, id):
#     current_user = User.objects.get(username=request.user)
#     count_cart = Cart.objects.filter(user_id=current_user.id).count()
#     count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
#     poja = Pooja.objects.get(id=id)
#     print(poja)
#     caloffer=(float(poja.price)*float(poja.offers))/100
#     cal=float(poja.price)-caloffer
#     slottime = PoojaSlot.objects.all()
#     return render(request, "pujadetail.html", {'detailpoja':poja,'slot':slottime,'cart':count_cart,'pooja':count_puja, 'cal':cal})

def ViewPujaDetail(request, id):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        prod = Pooja.objects.get(id=id)
        print(prod.price)
        print(prod.offers)
        caloffer=(float(prod.price)*float(prod.offers))/100
        cal=float(prod.price)-caloffer
        slottime = PoojaSlot.objects.all()
        ob = Pooja.objects.filter(id=id)
        ob.update(offerprice=cal)
        return render(request, "pujadetail.html", {'detailpoja':prod,'slot':slottime,'cart':count_cart,'pooja':count_puja,'cal':cal})
    except User.DoesNotExist:
        poja = Pooja.objects.get(id=id)
        print(poja)
        slottime = PoojaSlot.objects.all()
        return render(request, "pujadetail.html", {'detailpoja':poja,'slot':slottime})

# def AddPoojaSlot(request, id):
#     try:
#         user = User.objects.get(username=request.user)    #current user access anywhere
#         obj = Pooja.objects.get(id=id)
        
#         c = PujaSlotBooking(user=user, pooja=obj)
#         c.save()
#         #(request, "Puja slot booked successfully...  ")
#         return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
#     except:
#         return redirect('/login/')
#         # #(request, "Puja slot already booked!!!")
#         # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
        
        
def AddPoojaSlot(request, id):
    # print('gazskdhgi;sudghaordgjtsegvofdigjodfojgljgjdfdgodfodfoiohgidifihoig',str(request.user))
    # if str(request.user)=='AnonymousUser':
    #     return redirect('/login/')
    # else:
    try:
        
        
        user = User.objects.get(username=request.user)    #current user access anywhere
        obj = Pooja.objects.get(id=id)
        print('ksdhbchjk',user)
        print('jhdbch   ',obj)
        if request.method =="POST":
            user=request.user
            slot = request.POST['pujaslt']
            date = request.POST['date']
            pujaid = obj

            if PujaSlotBooking.objects.filter(user=user,pooja=pujaid).first():
                messages.info(request, 'Puja slot is already booked')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
            
            c = PujaSlotBooking(user=user, pooja=pujaid, pujaslot_id=slot, dateofpuja=date)
            c.save()
            messages.success(request, "You have successfully added puja in your cart.")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))        
            
        else:
            # (request, "Puja slot already booked")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))    
    except User.DoesNotExist:
             return redirect('/login/')
    # else:
    #     user=request.user
    #     slot = request.POST['pujaslt']
    #     date = request.POST['date']
    #     pujaid = request.POST['pujaid']

    #     c = PujaSlotBooking(user=user, pooja=pujaid, pujaslot=slot, dateofpuja=date)
    #     c.save()
    #     #(request, "Puja slot booked successfully...  ")
    #     print('jdkvje')
    #     #(request, "Something right!!!!!!!!")
    #     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
    #     print('difvujfnveq')
    #     #(request, "Something wrong!!!!!!!!")
    #     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
  
        # return redirect('/login/')
        # #(request, "Puja slot already booked!!!")
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 

def ViewPujadescription(request, id):
    current_user = User.objects.get(username=request.user)
    countcart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    detailprod = PujaSlotBooking.objects.get(id=id)
    print("YYUUHJJJJ HHJKJK",detailprod.pooja.price)
    return render(request, "pujadetailbyslot.html",{'detailprod':detailprod,'cart':countcart,'pooja':count_puja})
        
from web_astrology import settings
def ViewPujaSlotBooking(request):
    try:
        current_user = User.objects.get(username=request.user)
        countcart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        
        user = User.objects.get(id=request.user.id)
        print(user)
        prod = PujaSlotBooking.objects.filter(user_id=user.id).order_by('id').reverse()
        print("ddferfe fefefefe rfer",prod)
        pi = []
        for i in prod:
            i= pi.append(i.pooja.name)
        print("My Product", pi) 
        c = 0
        g = 0
        for i in prod:
            c = c + int(i.pooja.price)
            g = g + float(i.pooja.offerprice)
        print(c)   
        
        
        client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
        payment = client.order.create({ 'amount': g * 100, 'currency': 'INR', 'payment_capture': 1})
        print("******************************")
        print(payment)
        print("******************************")
        
        pujaid = pi
        usr = request.user.id
        date = datetime.now()
        # quantity= request.POST['qty']
        amount = payment['amount']/100
        razor_pay_order_id = payment['id']
        
        # orderobj = PoojaOrder(pujaid=pujaid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=False)
        # orderobj.save()
        # #(request, "Order created....")
            
        
        current_user = User.objects.get(username=request.user)
        # count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_cart = PujaSlotBooking.objects.filter(user_id=current_user.id)
    	# pujaslot = models.ForeignKey(PoojaSlot, on_delete=models.CASCADE)
        print('count_cart',count_cart[0].pujaslot)
        # return render(request, "showpujaslot.html", {'cartprod':prod, 'item':count_cart, 'totzalamt':c, 'payment':payment})
        
        
            
        return render(request, "showpujaslot.html", {'cartprod':prod, 'slot':count_cart[0].pujaslot,'slot1':count_cart[0].dateofpuja,'totalamt':c, 'totalamt1':g, 'payment':payment,'cart':countcart,'pooja':count_puja})
    except:
        return render(request, 'showpujaslot.html')
        
        
        
        
    
    
# def AddToCart(request, id):
    
#     # print(user)
#     # print(obj)
#     try:
#         user = User.objects.get(username=request.user)    #current user access anywhere
#         obj = Products.objects.get(id=id)
#         if request.method=='POST':
#             qty=request.POST['quantity']
            
#             if Cart.objects.filter(user=user,product=obj).exists():
#                 messages.info(request, 'Puja slot is already booked')
#                 return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
        
#             c = Cart(user=user, product=obj,quantity=qty)
#             c.save()
#             #(request, "Cart create successfully...  ")
#             return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
        
#         else:
#             #(request, "Something went wrong!")
#             return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))    
#     except User.DoesNotExist:
#              return redirect('/login/')


        # #(request, "Cart already created!!!")
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 




def AddToCart(request, id):
    # print(user)
    # print(obj)
    try:
        current_user = User.objects.get(username=request.user)
        countcart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        user = User.objects.get(username=request.user)    #current user access anywhere
        obj = Products.objects.get(id=id)
        print('obj.quantity',obj.quantity)
        if request.method=='POST':
            qty=request.POST['quan']
            if Cart.objects.filter(user=user,product=obj).exists():
                # messages.info(request, 'Puja slot is already booked')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            print('qty',qty)
            c = Cart(user=user, product=obj,quantity=qty)
            c.save()
            prodquantity=int(obj.quantity)-int(qty)
            print(prodquantity)
            obj1 = Products.objects.filter(id=id)
            obj1.update(quantity=prodquantity)
            # messages.success(request, "Cart create successfully...  ")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'),{'cart':countcart,'pooja':count_puja})
        else:
            messages.success(request, "Something went wrong!")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    except User.DoesNotExist:
             return redirect('/login/')
        # messages.success(request, "Cart already created!!!")
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
        
        
def ViewProductdescription(request, id):
    current_user = User.objects.get(username=request.user)
    countcart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    if request.method == 'POST':
        qty=request.POST['quan']
        
        uplead = Cart.objects.filter(id=id)
        
        uplead.update(quantity=qty)
        messages.success(request, f"Updated Successfully")
        # return redirect('/superadmin/edit_leadinfo//')
        return redirect('/showcart/') 
    else:
        detailprod = Cart.objects.get(id=id)
        print("YYUUHJJJJ HHJKJK",detailprod.product.price)
        
        caloffer=(float(detailprod.product.price)*float(detailprod.product.offers))/100
        cal=float(detailprod.product.price)-caloffer
        prodquan=int(detailprod.product.quantity)   
        
        return render(request, "productdetailbycart.html",{'detailprod':detailprod,'cal':cal, 'prodquan':prodquan, 'cart':countcart,'pooja':count_puja})

from web_astrology import settings
# def ViewCartProduct(request):
#     try:
#         user = User.objects.get(id=request.user.id)
#         print(user)
#         prod = Cart.objects.filter(user_id=user.id).order_by('id').reverse()
#         print(prod)
#         pi = []
#         for i in prod:
#             i= pi.append(i.product.prodname)
#         print("My Product", pi) 
#         c = 0
#         for i in prod:
#             c = c + int(i.product.price)
#         print(c)   
        
        
#         ls = []
#         tot = 0
#         for pro in prod:
#             print('Thisssssss',type(pro.product.price))
#             amt = float(pro.product.price)
#             qty = int(pro.quantity)
#             print("wedfefefefef feff",type(amt))
#             # pro = ls.append(amt)
#             # qty = ls.append(qty)
#             total = amt*qty
#             ls.append(total)
#             tot = sum(ls)
            
#             print(tot)
            
#             mylist = zip(prod, ls)
        
#         # client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
#         # payment = client.order.create({ 'amount': tot * 100, 'currency': 'INR', 'payment_capture': 1})
#         # print("******************************")
#         # print(payment)
#         # print("******************************")
        
#         # prodid = pi
#         # usr = request.user.id
#         # date = datetime.now()
#         # # quantity= request.POST['qty']
#         # amount = payment['amount']/100
#         # razor_pay_order_id = payment['id']
        
#         # orderobj = Order(productid=prodid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=False)
#         # orderobj.save()
#         # # #(request, "Order created....")
            
        
     
#         # print(tot)  
#         # print(ls)
        
#         current_user = User.objects.get(username=request.user)
#         count_cart = Cart.objects.filter(user_id=current_user.id).count()
#         return render(request, "showcart.html", {'cartprod':prod, 'item':count_cart, 'totalamt':c, 'mylist':mylist,'tot':tot})
#     except:
#         return render(request, 'showcart.html')
        
def ViewCartProduct(request):
    try:
        current_user = User.objects.get(username=request.user)
        countcart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        
        user = User.objects.get(id=request.user.id)
        print(user)
        prod = Cart.objects.filter(user_id=user.id).order_by('id').reverse()
        print(prod)
        pi = []
        for i in prod:
            i= pi.append(i.product.prodname)
        print("My Product", pi) 
        print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]')
        c = 0
        for i in prod:
            c = c + float(i.product.offerprice)
        print('======================',c)   
        
        
        
        ls = []
        tot = 0
        for pro in prod:
            print('Thisssssss',type(pro.product.offerprice))
            amt = float(pro.product.offerprice)
            qty = int(pro.quantity)
            print("wedfefefefef feff",type(amt))
            # pro = ls.append(amt)
            # qty = ls.append(qty)
            total = amt*qty
            ls.append(total)
            tot = sum(ls)
            
            print(tot)
            
            mylist = zip(prod, ls)
        
        # client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
        # payment = client.order.create({ 'amount': tot * 100, 'currency': 'INR', 'payment_capture': 1})
        # print("******************************")
        # print(payment)
        # print("******************************")
        
        # prodid = pi
        # usr = request.user.id
        # date = datetime.now()
        # # quantity= request.POST['qty']
        # amount = payment['amount']/100
        # razor_pay_order_id = payment['id']
        
        # orderobj = Order(productid=prodid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=False)
        # orderobj.save()
        # # #(request, "Order created....")
            
        
     
        # print(tot)  
        # print(ls)
        
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        return render(request, "showcart.html", {'cartprod':prod, 'item':count_cart, 'totalamt':c, 'mylist':mylist,'tot':tot,'cart':countcart,'pooja':count_puja})
    except:
        return render(request, 'showcart.html')
        
        
        

def OrderPlaceAddres(request):
    #-===================================
        current_user = User.objects.get(username=request.user)
        countcart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    
        if request.method == 'POST':
            addre = request.POST['address']
            mobileno = request.POST['mobileno']
            houseno = request.POST['houseno']
            area = request.POST['area']
            landmark = request.POST['landmark']
            pincode = request.POST['pincode']
            towncity = request.POST['towncity']
            state = request.POST['state']
            usr  = request.user.id
            
            uplead = User.objects.filter(id=usr)
            
            uplead.update(currentaddress=addre,mobileno=mobileno,
                          houseno=houseno,area=area,landmark=landmark,pincode=pincode,
                          towncity=towncity)
            # orderobj.save()
            return redirect('/checkout/')
            
        else:
            usr  = request.user.id
            getUser = User.objects.get(id=usr) 
            # uplead = User.objects.filter(id=usr)
        return render(request, "orderaddress.html",{'getUser':getUser,'cart':countcart,'pooja':count_puja})
    

    
    
    
def Checkout(request):
    
    current_user = User.objects.get(username=request.user)
    countcart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    user = User.objects.get(id=request.user.id)
    prod11 = PayByWalletAmount.objects.get(userid=user)
    cb = prod11.walletid
    # for i in prod11:
    #     print('i',i.amount)
    #     cb = cb + float(i.amount)
    # print(cb)
    print(user)
    prod = Cart.objects.filter(user_id=user.id).order_by('id').reverse()
    print(prod)
    pi = []
    for i in prod:
        i= pi.append(i.product.prodname)
    print("My Product", pi) 
    c = 0
    for i in prod:
        c = c + float(i.product.offerprice)
    print(c)   
    
    
    qt = 0
    for i in prod:
        qt+=int(i.quantity)
           
    ls = []
    tot = 0
    for pro in prod:
        print('Thisssssss',type(pro.product.offerprice))
        amt = float(pro.product.offerprice)
        qty = int(pro.quantity)
        print("wedfefefefef feff",type(amt))
        # pro = ls.append(amt)
        # qty = ls.append(qty)
        total = amt*qty
        ls.append(total)
        tot = sum(ls)
        
        print(tot)
        
        mylist = zip(prod, ls)
    # if float(cb)>=float(tot):
    
    client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
    payment = client.order.create({ 'amount': tot * 100, 'currency': 'INR', 'payment_capture': 1})
    print("******************************")
    print(payment)
    print("******************************")
    
    prodid = pi
    usr = request.user.id
    date = datetime.now()
    # quantity= request.POST['qty']
    amount = payment['amount']/100
    razor_pay_order_id = payment['id']
    # address = addr.address
    
    orderobj = Order(productid=prodid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=False,address=request.user.currentaddress,quantity=qt)
    orderobj.save()
    # messages.success(request, "Order created....")
    
    # After Checkout cart will 0
    # prod.delete()

    print(tot)  
    print(ls)
    
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    return render(request, "checkout.html", {'cb':float(cb),'tot':float(tot),'cartprod':prod, 'item':count_cart, 'totalamt':c, 'payment':payment, 'mylist':mylist,'tot':tot,'cart':countcart,'pooja':count_puja})
    # return render(request, "checkout.html")
    # else:
    #     return render(request, "incufficient.html")




def QusAndAnswerView(request):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        
        quscat = CategoryOfFAQ.objects.all()
        time = AnswerFAQTime.objects.all()
        current_user = User.objects.get(username=request.user)
        profiles = FamilyFriendsprofile.objects.filter(ask_by=current_user)
        
        
        if request.method == 'POST':
            catname = request.POST['category']
            timing = request.POST['answertime']
            qus = request.POST['qus']
            # username = request.user.id
            username = request.POST['ask_qus']
            date = datetime.now()
            
            
            
            user_obj = QusAndAnswer(category_id=catname, answertime_id=timing, qus=qus, userid_id=request.user.id,ask_date=date,friend=username)
            user_obj.save()
            
            #(request, 'Pay here to get answer successfully.')
            return redirect('/askquestionpay/')
        else:
            return render(request, "askquestion.html", {'cate':quscat, 'anstime':time, 'relation':profiles,'cart':count_cart,'pooja':count_puja})
    except User.DoesNotExist:
             return redirect('/login/')
            
            
    
def QusAndAnswerViewPayment(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    prod11 = PayByWalletAmount.objects.get(userid=user)
    cb = prod11.walletid
    
    quscat = CategoryOfFAQ.objects.all()
    time = AnswerFAQTime.objects.all()
    current_user = User.objects.get(username=request.user)
    profiles = FamilyFriendsprofile.objects.filter(ask_by=current_user)
    
    
    prod = QusAndAnswer.objects.filter(userid=user.id)
    print(prod[len(prod)-1].id)
    
    
    # pi = []
    # for i in prod:
    #     i= pi.append(i.id)
    # print("My Product", pi)
    c = 0
    for i in prod:
        c = int(i.answertime.price)
    print(type(c))  
    
    # if float(cb)>=float(c):
    
    client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
    payment = client.order.create({ 'amount': c * 100, 'currency': 'INR', 'payment_capture': 1})
    print("******************************")
    print(payment['amount'])
    print("******************************")    
    
    # pi = []
    # for i in prod:
    #     i= pi.append(i.askqusid)
    # print("My Product", pi) 
    qustion = prod[len(prod)-1].qus
    prodid = prod[len(prod)-1].id
    usr = request.user.id
    date = datetime.now()
    # quantity= request.POST['qty']
    amount = payment['amount']/100
    razor_pay_order_id = payment['id']
    
    orderobj = QusAndAnswerPayment(askqusid_id=prodid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=True)
    orderobj.save()
    
    # updt = QusAndAnswer.objects.filter(id=id)
    prod.update(is_paid=True)


    # return redirect('/askquestion/')
    
    return render(request, "checkoutforqa.html", {'cb':float(cb),'tot':float(c),'cate':quscat, 'anstime':time, 'relation':profiles,'cart':count_cart,'pooja':count_puja, 'payment':payment,'qustion':qustion,'amount':amount})
# else:
    #     return render(request, "incufficient.html")
 
def ShowProfileDetail(request):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        current_user = User.objects.get(username=request.user)
        return render(request, "profile.html", {"user":current_user,'cart':count_cart,'pooja':count_puja})
    except User.DoesNotExist:
             return redirect('/login/')
    
    
def ShowFAQReply(request):   
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        user = User.objects.get(id=request.user.id)
        faq = QusAndAnswer.objects.filter(userid=user).order_by('-id')
        
        paginator = Paginator(faq, 6)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        totalpage = all_lead.paginator.num_pages
        # for i in all_lead:
        #     print(i)
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'faq':faq,
            'cart':count_cart,
            'pooja':count_puja
        }
        return render(request, "faqanswer.html", context)
    except User.DoesNotExist:
             return redirect('/login/')

def ShowOrderlist(request):   
    try:
        
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        user = User.objects.get(id=request.user.id)
        prodord = Order.objects.filter(userid=user).order_by('-id')
        
        paginator = Paginator(prodord, 6)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        totalpage = all_lead.paginator.num_pages
        # for i in all_lead:
        #     print(i)
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'cart':count_cart,
            'pooja':count_puja
        }
        return render(request, "userproductorder.html", context)
    except User.DoesNotExist:
             return redirect('/login/')


def ShowPojaSlot(request):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        user = User.objects.get(id=request.user.id)
        pujaord = PoojaOrder.objects.filter(userid=user).order_by('-id')
        
        paginator = Paginator(pujaord, 6)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        totalpage = all_lead.paginator.num_pages
        # for i in all_lead:
        #     print(i)
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'cart':count_cart,
            'pooja':count_puja,
            'pujaord':pujaord
        }
        return render(request, "userpujaorder.html", context)
    except User.DoesNotExist:
             return redirect('/login/')
    

def ShowFaqPayment(request):
    try:
        current_user = User.objects.get(username=request.user)
        count_cart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        user = User.objects.get(id=request.user.id)
        faqpay = QusAndAnswerPayment.objects.filter(userid=user).order_by('-id')
        
        paginator = Paginator(faqpay, 6)
        page_number = request.GET.get('page')
        all_lead = paginator.get_page(page_number)
        totalpage = all_lead.paginator.num_pages
        # for i in all_lead:
        #     print(i)
        context = {
            'all_lead':all_lead,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)],
            'cart':count_cart,
            'pooja':count_puja,
            'faqpay':faqpay
        }
        return render(request, "useruespayment.html", context)
    except User.DoesNotExist:
             return redirect('/login/')
    
def UserRegister(request):
    code = CountryCode.objects.all()
    if request.method == 'POST':
        name = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['usernm']
        password = request.POST['password']
        profilimg = request.FILES['profile']
        gend = request.POST['gender']
        phone = request.POST['contact']
        code = request.POST['code']
        lang = request.POST['language']
        birthdate = request.POST['dob']
        marid = request.POST['marital']
        birthtime = request.POST['timebirth']
        place = request.POST['place']
        addr = request.POST['address']
        date = datetime.now()
        try:
            if User.objects.filter(username = username).first():
                #(request, 'Username is already exist.')
                return redirect('/register/')

            if User.objects.filter(email = email).first():
                #(request, 'Email is already exist.')
                return redirect('/register/')
            
            user_obj = User(first_name=name, 
                            last_name=lname, 
                            email=email, 
                            username=username, 
                            password=make_password(password), 
                            profilepicture=profilimg, 
                            is_user=True, 
                            date_joined=date,
                            contactno=phone,
                            countrycode=code,
                            gender=gend,
                            language=lang,
                            dateofbirth=birthdate,
                            marital_status=marid,
                            timeofbirth=birthtime,
                            placeofbirth=place,
                            currentaddress=addr
                            )
            user_obj.save()
            messages.success(request, 'Username is register successfully.')
            return redirect('/register/')
            

        except Exception as e:
            print(e)
            return redirect('/register/')
    else:
        return render(request, "user_register.html",{'code':code})


def EditProfileView(request, id):
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    
    uplead = User.objects.filter(id=id)
    uplead1 = User.objects.get(id=id)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['usernm']
        contact = request.POST['phoneno']
        # code = request.POST['code']
        gend = request.POST['gender']
        lang = request.POST['language']
        birthdate = request.POST['dob']
        marid = request.POST['marital']
        birthtime = request.POST['timebirth']
        place = request.POST['place']
        addr = request.POST['address']
        
        if len(request.FILES) !=0:
            if len(uplead1.profilepicture) > 0:
                print('yessssssssssssssss1')
                os.remove(uplead1.profilepicture.path)
                # print(uplead1.profilepicture.path)
            uplead1.profilepicture = request.FILES['profilep']
            uplead1.save()
        
        uplead = User.objects.filter(id=id)
        
        uplead.update(first_name=fname,
                        last_name=lname,
                        email=email,
                        username=username,
                        contactno=contact,
                        # countrycode=code,
                        gender=gend,
                        language=lang,
                        dateofbirth=birthdate,
                        marital_status=marid,
                        timeofbirth=birthtime,
                        placeofbirth=place,
                        currentaddress=addr
                        )
        #(request, f"{fname}, profile updated successfully")
        # return redirect('/superadmin/edit_leadinfo//')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  
    else:
        getUser = User.objects.get(id=id)    
        return render(request, "edituser.html", {'user':getUser,'cart':count_cart,'pooja':count_puja})


def FamilyFriendCreate(request):
    relation = Relationship.objects.all()
    if request.method == 'POST':
        name = request.POST['fname']
        lname = request.POST['lname']
        gend = request.POST['gender']
        rel = request.POST['relation']
        birthdate = request.POST['dob']
        birthtime = request.POST['timebirth']
        place = request.POST['place']
        user = request.user.id
        
            
        user_obj = FamilyFriendsprofile(first_name=name, 
                        lastname=lname, 
                        gender=gend,
                        relationship_id=rel,
                        dateofbirth=birthdate,
                        timeofbirth=birthtime,
                        placeofbirth=place,
                        ask_by_id=user
                        )
        user_obj.save()
        #(request, 'Profile is create successfully.')
        return redirect('/getfriendfunction/')
         
    else:
        return render(request, "friendsprofile.html", {'relation':relation})
        
        
    

def AddFriendView(request):
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    
    user = User.objects.get(id=request.user.id)
    getcreate = FamilyFriendsprofile.objects.filter(ask_by=user)#.order_by('id')
    return render(request, "getfamilyfriend.html", {'getdata':getcreate,'cart':count_cart,'pooja':count_puja})
    
    
def EditFriendProfileView(request, id):
    relation = Relationship.objects.all()
    if request.method == 'POST':
        name = request.POST['fname']
        lname = request.POST['lname']
        gend = request.POST['gender']
        rel = request.POST['relation']
        birthdate = request.POST['dob']
        birthtime = request.POST['timebirth']
        place = request.POST['place']
        user = request.user.id
        
        
        
        
        uplead = FamilyFriendsprofile.objects.filter(id=id)
        
        uplead.update(first_name=name, 
                        lastname=lname, 
                        gender=gend,
                        relationship_id=rel,
                        dateofbirth=birthdate,
                        timeofbirth=birthtime,
                        placeofbirth=place,
                        ask_by_id=user
                        )
        messages.success(request, f"{name}, profile updated successfully")
        return redirect('/getfriendfunction/')
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  
    else:
        getUser = FamilyFriendsprofile.objects.get(id=id)    
        return render(request, "editfriendsprofile.html", {'user':getUser, 'relation':relation})



def DeleteFriendProfile(request, id):
    data = FamilyFriendsprofile.objects.get(id=id)
    data.delete()
    # messages.success(request, f"{data.product.prodname}, has been deleted succsessfull")
    return redirect('/getfriendfunction/')

    
    

def GetOrderView(request):
    user = User.objects.get(id=request.user.id)
    getcreate = Order.objects.filter(userid=user)#.order_by('id')
    print(getcreate)
    return render(request, "productorderlist.html", {'getorderlist':getcreate})




def DailyBlosView(request):
    bloglist = DailyBlogs.objects.all()
    return render(request, "blog_single.html", {'blog':bloglist})

def SendCustomerSupport(request):
    try:
        current_user = User.objects.get(username=request.user)
        countcart = Cart.objects.filter(user_id=current_user.id).count()
        count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
        if request.method == "POST":
            user = request.user.id
            msg = request.POST['message']
    
            user_obj = CustomerSupport(userid_id=user,message=msg)
            user_obj.save()
            #(request, 'Submitted successfully.')
            return redirect('/customersupport/')
        return render(request, "customersupport.html",{'cart':countcart,'pooja':count_puja})
    except:
             return redirect('/login/')
def HoroscopeView(request):
    # Parse the input string into a datetime object
    input_string = datetime.now()
    input_datetime = input_string.strftime('%Y-%m-%dT%H:%M:%SZ')
    # Format the datetime object into the desired format
    # output_format = '%Y-%m-%dT%H:%M:%SZ'
    # formatted_datetime = input_datetime.strftime(output_format)
    print('formatted_datetime',input_datetime)
    payload={'grant_type':'client_credentials',
             'client_id':'bc4cc437-7426-46d8-b2a9-fea839b73140',
             'client_secret':'CrCHJZTAjyRZwYBiNUbiwimrtyDJEI1FcncTaXyS'}
    r = requests.post('https://api.prokerala.com/token',data=payload)
    rq=r.json()
    print(rq['access_token'])
    authh =rq['token_type']+' '+rq['access_token']
    payload = {'datetime': input_datetime, 'sign': 'leo'}
    headers = {'Authorization': authh}
    r1 = requests.get('https://api.prokerala.com/v2/horoscope/daily', params=payload, headers=headers)
    print(r1.json())
    rq1=r1.json()
    print(rq1['data']['daily_prediction']['prediction'])
    return render(request,'customersupport.html')


def FilterHoroscopeByCategory(request,id):
    try:
        # catname = HoroscopeCategory.objects.all()
        cateid  = HoroscopeCategory.objects.get(id=id)
        print("category ", str(cateid))
        catfilter = Horoscope.objects.filter(horscopname=cateid)
        # print("My category",catfilter[0].catname)
        input_string = datetime.now()
        input_datetime = input_string.strftime('%Y-%m-%dT%H:%M:%SZ')
        # Format the datetime object into the desired format
        # output_format = '%Y-%m-%dT%H:%M:%SZ'
        # formatted_datetime = input_datetime.strftime(output_format)
        print('formatted_datetime',input_datetime)
        payload={'grant_type':'client_credentials',
                #  'client_id':'65f7cd47-2762-4de2-a1af-a6916f3309a3',
                #  'client_secret':'5Ntne0tHhFsORHX0sQfu0uOjnauVhxffbxsYnzKP'}
                  'client_id':'91a1b3fa-780b-4cc5-bf46-96d37ac7d2fa',
                 'client_secret':'yt5IwjxKvr5cm1eDuaAmtzbButm5RbW35SIpNqLI'}
        r = requests.post('https://api.prokerala.com/token',data=payload)
        rq=r.json()
        print(rq['access_token'])
        authh =rq['token_type']+' '+rq['access_token']
        payload = {'datetime': input_datetime, 'sign': str(cateid).lower()}
        headers = {'Authorization': authh}
        r1 = requests.get('https://api.prokerala.com/v2/horoscope/daily', params=payload, headers=headers)
        print(r1.json())
        rq1=r1.json()
        # print(rq1['data']['daily_prediction']['prediction'])
        rqqcon=rq1['data']['daily_prediction']['prediction']
        return render(request, "horoscope_single.html", {'catid':cateid, 'catfilter':catfilter, 'content':rqqcon})
        # return render(request, "horoscope_single.html", {'catid':cateid, 'catfilter':catfilter})
    except KeyError:
        return redirect('/')
    
    
    
def DeleteCart(request, id):
    data = Cart.objects.get(id=id)
    data.delete()
    #(request, f"{data.product.prodname}, has been deleted succsessfull")
    return redirect('/showcart/')


def DeletePoja(request, id):
    data = PujaSlotBooking.objects.get(id=id)
    data.delete()
    #(request, f"{data.pooja.name}, has been deleted succsessfull")
    return redirect('/pujaslot/')

def AddWalletAmount(request):
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    user = User.objects.get(id=request.user.id)
    qapay = QusAndAnswerPayment.objects.filter(userid=request.user.id,razor_pay_order_id='Wallet')
    prodpay = Order.objects.filter(userid=request.user.id,razor_pay_order_id='Wallet')
    pujapay = PoojaOrder.objects.filter(userid=request.user.id,razor_pay_order_id='Wallet')
    
    p=0
    for m in qapay:
        p=p+float(m.order_price)
    
    
    q=0
    for n in prodpay:
        q=q+float(n.order_price)
    
    
    r=0
    for o in pujapay:
        r=r+float(o.order_price)
    
    # for m,n,o in zip(qapay,prodpay,pujapay):
    #     #  p=p+float(m.order_price)
    #      q=q+float(n.order_price)
    #      r=r+float(o.order_price)
   
    z=p+q+r
    
    prod = WalletAmt.objects.filter(userid=user)
    c = 0
    for i in prod:
        c = c + float(i.amount)
    
        
    uss=PayByWalletAmount.objects.filter(userid_id=request.user.id).exists()
    # print(uss.walletid)
    # var2=PayByWalletAmount.objects.get(userid_id=user)
    

    if uss:
        var2=PayByWalletAmount.objects.get(userid_id=user)
        chg=float(var2.walletid)
    else:
        chg=0
    
    
    if request.method == "POST":
        user = request.user.id
        amount = request.POST['amount']
        var = WalletAdd(userwallet_id=user, walletamount=amount)
        var.save()
        
        messages.success(request, "Add wallet amount successfull..")
        return redirect('/paymentadmin/')
    return render(request, "walletamount.html", {'amount':prod, 'amt':chg,'cart':count_cart,'pooja':count_puja})


def PaymentByRazorpay(request):
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    user = User.objects.get(id=request.user.id)
    prod = WalletAdd.objects.filter(userwallet=user)
    
    
    # pi = []
    # for i in prod:
    #     i= pi.append(i.id)
    # print("My Product", pi)
    c1 = 0
    for i in prod:
        c1 = int(i.walletamount)
        
    qapay = QusAndAnswerPayment.objects.filter(userid=request.user.id,razor_pay_order_id='Wallet')
    prodpay = Order.objects.filter(userid=request.user.id,razor_pay_order_id='Wallet')
    pujapay = PoojaOrder.objects.filter(userid=request.user.id,razor_pay_order_id='Wallet')
    
    
    p=0
    for m in qapay:
        p=p+float(m.order_price)
    
    q=0
    for n in prodpay:
        q=q+float(n.order_price)
    
    r=0
    for o in pujapay:
        r=r+float(o.order_price)
        
        
    z=p+q+r
    prod2 = WalletAmt.objects.filter(userid=user)
    c = 0
    for i in prod2:
        c = c + float(i.amount)
    
    
    client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
    payment = client.order.create({ 'amount': c1 * 100, 'currency': 'INR', 'payment_capture': 1})   
    
    # pi = []
    # for i in prod:
    #     i= pi.append(i.askqusid)
    # print("My Product", pi) 
    
    prodid = prod[0].id
    print("prodid", prodid)
    usr = request.user.id
    date = datetime.now()
    # quantity= request.POST['qty']
    amount = payment['amount']/100
    razor_pay_order_id = payment['id']
    if request.method == "POST":
        payid = request.POST.get('razorpay_payment_id')
        signatur = request.POST.get('razorpay_signature')
        # Now you can use payid and signatur in your logic
        # For example, you can update the WalletAmt model with these values
        
        if signatur and payid:
            uss=PayByWalletAmount.objects.filter(userid_id=request.user.id).exists()
            print('hcawdskj',uss)
            am = (float(c)-float(z))+float(amount)
            if uss:
                var2=PayByWalletAmount.objects.filter(userid_id=user)
                var2.update(walletid=am)
            else:
                var1 = PayByWalletAmount(userid_id=user, walletid=am)
                var1.save()
            
            orderobj = WalletAmt(walt_id=prodid,userid_id=usr,amount=amount,orderdate=date,razor_pay_order_id=razor_pay_order_id,order_status=True,razor_pay_payment_id=payid, razor_pay_payment_signature=signatur)
            orderobj.save()
        else:
            pass

    messages.success(request, 'Pay successfully.')
    # return redirect('/askquestion/'))
    return render(request, "walletcash.html", {'payment':payment,'cart':count_cart,'pooja':count_puja,'amount':amount})



    
def PayWithWallet(request):
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    count_puja = PujaSlotBooking.objects.filter(user_id=current_user.id).count()
    user = User.objects.get(id=request.user.id)
    print(user)
    prod23 = WalletAmt.objects.filter(userid=user)
    cb = 0
    for i in prod23:
        print('i',i.amount)
        cb = cb + float(i.amount)
        
    print(cb)
    print("=================",request.user.currentaddress)
    user = User.objects.get(id=request.user.id)
    print(user)
    # addr = OrderPlaceAddress.objects.filter(userid=user)
    # print("dsfsfsfsd",addr)
    prod = Cart.objects.filter(user_id=user.id).order_by('id').reverse()
    print(prod)
    pi = []
    for i in prod:
        i= pi.append(i.product.prodname)
    print("My Product", pi) 
    c = 0
    for i in prod:
        c = c + float(i.product.offerprice)
 
    
    ls = []
    tot = 0
    for pro in prod:
        print('Thisssssss',type(pro.product.offerprice))
        amt = float(pro.product.offerprice)
        qty = int(pro.quantity)
        print("wedfefefefef feff",type(amt))
        # pro = ls.append(amt)
        # qty = ls.append(qty)
        total = amt*qty
        ls.append(total)
        tot = sum(ls)
        
        print(tot)
        
        mylist = zip(prod, ls)
    

    prodid = pi
    usr = request.user.id
    date = datetime.now()
    # quantity= request.POST['qty']
    amount = tot
    razor_pay_order_id = 'Wallet'
    
    orderobj = Order(productid=prodid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=False,address=request.user.currentaddress)
    orderobj.save()
    # # messages.success(request, "Order created....")
    
    # prod.delete()
        
    # current_user = User.objects.get(username=request.user)
    # count_cart = Cart.objects.filter(user_id=current_user.id).count()
    # return render(request, "paywithwallet.html", {'cartprod':prod, 'item':count_cart, 'totalamt':tot, 'payment':payment, 'mylist':mylist,'tot':tot, 'ggg':cb})
    upl = PayByWalletAmount.objects.get(userid=request.user.id)
    ll=upl.walletid
    amtminus=float(upl.walletid)-float(tot)
    uplead = PayByWalletAmount.objects.filter(userid=usr)
        
    uplead.update(walletid=amtminus)
    # py12=PayByWalletAmount.objects.get(id=request.user.id)
    # print('edhfcewkfjehn',py12.walletid)
    
    return render(request, "paywithwallet.html", {'ggg':cb,'cartprod':prod, 'll':ll, 'totalamt':tot, 'amtt':amtminus,'cart':count_cart,'pooja':count_puja})
    
    # return render(request, "checkout.html")
    
def CheckoutforPuja(request):
    
    user = User.objects.get(id=request.user.id)
    print(user)
    prod11 = PayByWalletAmount.objects.get(userid=user)
    cb = prod11.walletid
    print("=================",request.user.currentaddress)
    user = User.objects.get(id=request.user.id)
    print(user)
    addr = OrderPlaceAddress.objects.filter(userid=user)
    print("dsfsfsfsd",addr)
    prod = PujaSlotBooking.objects.filter(user_id=request.user.id).order_by('id').reverse()
    print(';kdjdhfoILejf    poewfigwel;hger;lkgkhffoksdljhairuhrepokk',prod)
    pi = []
    for i in prod:
        pi.append(i.pooja.name)
    print("My Product", pi) 
    
    pd=[]
    for i in prod:
        pd.append(i.dateofpuja)
    print("My Puja Date >>>>>>>>>>>>>>>>>>>>>>", pd) 
    
    c = 0
    for i in prod:
        c = c + float(i.pooja.offerprice)
 
    
    ls = []
    tot = 0
    for pro in prod:
        print('Thisssssss',type(pro.pooja.offerprice))
        amt = float(pro.pooja.offerprice)
        # qty = int(pro.quantity)
        print("wedfefefefef feff",type(amt))
        # pro = ls.append(amt)

        
        ls.append(amt)
        tot = sum(ls)
        
        print(tot)
        
        mylist = zip(prod, ls)
      

    client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
    payment = client.order.create({ 'amount': tot * 100, 'currency': 'INR', 'payment_capture': 1})
    print("******************************")
    print(payment)
    print("******************************")
    
    pujadate = pd
    prodid = pi
    usr = request.user.id
    date = datetime.now()
    # quantity= request.POST['qty']
    amount = payment['amount']/100
    razor_pay_order_id = payment['id']

    
    orderobj = PoojaOrder(pujaid=prodid,userid_id=usr,orderdate=date,order_price=amount,bookeddate=pujadate,razor_pay_order_id=razor_pay_order_id,order_status=False,address=request.user.currentaddress)
    orderobj.save()
    # messages.success(request, "Order created....")
    
    # prod.delete()
    

    # print(tot)  
    # print(ls)
    # if cb > tot:
    #     var =  cb - tot
    #     print(var)
    #     uplead = WalletAdd.objects.filter(userwallet=request.user.id)
            
    #     uplead.update(walletamount=int(var))
        
    # else:
    #     print('Invalit Amount')
        
    
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    return render(request, "checkoutforpuja.html", {'cb':float(cb),'tot':float(tot),'cartprod':prod, 'item':count_cart, 'totalamt':tot, 'payment':payment, 'mylist':mylist,'tot':tot, 'ggg':cb})
    # return render(request, "checkout.html")

                # return render(request, "checkout.html")

def PayWithWalletforPuja(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    prod23 = WalletAmt.objects.filter(userid=user)
    cb = 0
    for i in prod23:
        print('i',i.amount)
        cb = cb + float(i.amount)
        
    print(cb)
    print("=================",request.user.currentaddress)
    user = User.objects.get(id=request.user.id)
    print(user)
    # addr = OrderPlaceAddress.objects.filter(userid=user)
    # print("dsfsfsfsd",addr)
    prod = PujaSlotBooking.objects.filter(user_id=user.id).order_by('id').reverse()
    print(prod)
    pi = []
    for i in prod:
        i= pi.append(i.pooja.name)
    print("My Product", pi) 
    c = 0
    for i in prod:
        c = c + float(i.pooja.offerprice)
 
    
    ls = []
    tot = 0
    for pro in prod:
        print('Thisssssss',type(pro.pooja.offerprice))
        amt = float(pro.pooja.offerprice)
        
        print("wedfefefefef feff",type(amt))
        
        ls.append(amt)
        tot = sum(ls)
        
        print(tot)
        
        mylist = zip(prod, ls)
    

    prodid = pi
    usr = request.user.id
    date = datetime.now()
    # quantity= request.POST['qty']
    amount = tot
    razor_pay_order_id = 'Wallet'
    
    orderobj = PoojaOrder(pujaid=prodid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=False,address=request.user.currentaddress)
    orderobj.save()
    # # messages.success(request, "Order created....")
    
    # prod.delete()
        
    # current_user = User.objects.get(username=request.user)
    # count_cart = Cart.objects.filter(user_id=current_user.id).count()
    # return render(request, "paywithwallet.html", {'cartprod':prod, 'item':count_cart, 'totalamt':tot, 'payment':payment, 'mylist':mylist,'tot':tot, 'ggg':cb})
    upl = PayByWalletAmount.objects.get(userid=request.user.id)
    ll=upl.walletid
    amtminus=float(upl.walletid)-float(tot)
    uplead = PayByWalletAmount.objects.filter(userid=request.user.id)
        
    uplead.update(walletid=amtminus)
    # py12=PayByWalletAmount.objects.get(id=request.user.id)
    # print('edhfcewkfjehn',py12.walletid)
    
    return render(request, "paywithwalletforpuja.html", {'ggg':cb,'cartprod':prod, 'll':ll, 'totalamt':tot, 'amtt':amtminus})
    
    # return render(request, "checkout.html")

def CheckoutforQA(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    prod11 = PayByWalletAmount.objects.get(userid=user)
    cb = prod11.walletid
    print("=================",request.user.currentaddress)
    user = User.objects.get(id=request.user.id)
    print(user)
    addr = OrderPlaceAddress.objects.filter(userid=user)
    print("dsfsfsfsd",addr)
    prod = QusAndAnswer.objects.filter(user_id=request.user.id).order_by('id').reverse()
    print(';kdjdhfoILejf    poewfigwel;hger;lkgkhffoksdljhairuhrepokk',prod)
    pi = []
    idd=[]
    for j in prod:
        idd.append(j.id)
    print('idd',max(idd))
    for i in prod:
        pi.append(i.pooja.name)
    print("My Product", pi) 
    c = 0
    for i in prod:
        c = c + float(i.pooja.price)
    
    ls = []
    tot = 0
    for pro in prod:
        print('Thisssssss',type(pro.pooja.price))
        amt = float(pro.pooja.price)
        # qty = int(pro.quantity)
        print("wedfefefefef feff",type(amt))
        # pro = ls.append(amt)

        
        ls.append(amt)
        tot = sum(ls)
        
        print(tot)
        
        mylist = zip(prod, ls)
    
    # client = razorpay.Client(auth = (settings.razor_pay_key_id, settings.key_secret) )
    # payment = client.order.create({ 'amount': tot * 100, 'currency': 'INR', 'payment_capture': 1})
    # print("******************************")
    # print(payment)
    # print("******************************")
    
    # prodid = pi
    # usr = request.user.id
    # date = datetime.now()
    # # quantity= request.POST['qty']
    # amount = payment['amount']/100
    # razor_pay_order_id = payment['id']
  
    
    # orderobj = PoojaOrder(pujaid=prodid,userid_id=usr,orderdate=date,order_price=amount,razor_pay_order_id=razor_pay_order_id,order_status=False,address=request.user.currentaddress)
    # orderobj.save()
    # messages.success(request, "Order created....")
    
    # prod.delete()
    

    # print(tot)  
    # print(ls)
    # if cb > tot:
    #     var =  cb - tot
    #     print(var)
    #     uplead = WalletAdd.objects.filter(userwallet=request.user.id)
            
    #     uplead.update(walletamount=int(var))
        
    # else:
    #     print('Invalit Amount')
        
    
    current_user = User.objects.get(username=request.user)
    count_cart = Cart.objects.filter(user_id=current_user.id).count()
    return render(request, "checkoutforqa.html", {'cb':float(cb),'tot':float(tot),'cartprod':prod, 'item':count_cart, 'totalamt':tot, 'payment':payment, 'mylist':mylist,'tot':tot, 'ggg':cb})
    # return render(request, "checkout.html")
    
def PayWithWalletforQA(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    prod23 = WalletAmt.objects.filter(userid=user)
    cb = 0
    for i in prod23:
        print('i',i.amount)
        cb = cb + float(i.amount)
        
    print(cb)
    print("=================",request.user.currentaddress)
    user = User.objects.get(id=request.user.id)
    print(user)
    # addr = OrderPlaceAddress.objects.filter(userid=user)
    # print("dsfsfsfsd",addr)
    prod = QusAndAnswer.objects.filter(userid=request.user.id).order_by('id').reverse()
    print(';kdjdhfoILejf    poewfigwel;hger;lkgkhffoksdljhairuhrepokk',prod)
    
    a=prod[0].qus
    b=prod[0].answertime.price
    c=prod[0].id
    # pi = []
    # idd=[]
    # for j in prod:
    #     idd.append(j.id)

    # print('idd',max(idd))
    # # prod = PujaSlotBooking.objects.filter(user_id=user.id).order_by('id').reverse()
    # # print(prod)
    # pi = []
    # for i in prod:
    #     pi.append(i.qus)
    # print("My Product", pi) 
    # c = 0
    # for i in prod:
    #     c = c + int(i.pooja.price)
 
    
    # ls = []
    # tot = 0
    # for pro in prod:
    #     print('Thisssssss',type(pro.pooja.price))
    #     amt = float(pro.pooja.price)
        
    #     print("wedfefefefef feff",type(amt))
        
    #     ls.append(amt)
    #     tot = sum(ls)
        
    #     print(tot)
        
    #     mylist = zip(prod, ls)
    

    # prodid = pi
    usr = request.user.id
    date = datetime.now()
    # quantity= request.POST['qty']
    amount = b
    razor_pay_order_id = 'Wallet'
    
    orderobj = QusAndAnswerPayment(askqusid_id = c,userid_id = request.user.id,orderdate = date,order_status = True,order_price = b,razor_pay_order_id = razor_pay_order_id)
    orderobj.save()
    # # messages.success(request, "Order created....")
    
    # prod.delete()
        
    # current_user = User.objects.get(username=request.user)
    # count_cart = Cart.objects.filter(user_id=current_user.id).count()
    # return render(request, "paywithwallet.html", {'cartprod':prod, 'item':count_cart, 'totalamt':tot, 'payment':payment, 'mylist':mylist,'tot':tot, 'ggg':cb})
    upl = PayByWalletAmount.objects.get(userid=request.user.id)
    ll=upl.walletid
    amtminus=float(upl.walletid)-float(b)
    uplead = PayByWalletAmount.objects.filter(userid=request.user.id)
        
    uplead.update(walletid=amtminus)
    # py12=PayByWalletAmount.objects.get(id=request.user.id)
    # print('edhfcewkfjehn',py12.walletid)
    
    return render(request, "paywithwalletforqa.html", {'ggg':cb,'cartprod':prod, 'll':ll, 'totalamt':b, 'amtt':amtminus})
    
    # return render(request, "checkout.html")
    
    
    
    
def SendMailToPassword(request):
    if request.method == 'POST':
        email = request.POST["email"]
        
        try:
            print("Hiiiiiiiiii")
            user = User.objects.get(email=email)
            print(user)
            print("Hello")
            send_mail(
                    'Response Mail',
                    f'Hi {user.first_name}, {user.last_name} \nWeclcome to Our Ask2Astro Your password change link here http://astro.techpanda.art/changeuserpassword/{user.id}/{user.username}',
                    'techpanda.sr@gmail.com',
                    [email],
                    fail_silently=False,
                )
            messages.success(request, "Check your email")
            return redirect('/mailpass/')
        except User.DoesNotExist:
            # Handle error case where the email is not found
            messages.success(request, "Email id not found.")
            return redirect('/mailpass/')        
   
    return render(request, "changepassform.html")



def UserForgotPassword(request,id,username):
    print(">>>>",id,username)
    usr = username
    
    
    
    oldpwd=User.objects.get(username=username)
    print('id',oldpwd.id)
    print('kdfjv',oldpwd.password)
    if request.method == "POST":
        newpwd = request.POST['newpassword']
        print(newpwd)
        uplead = User.objects.filter(id=id)
        print("working...............")
        uplead.update(password=make_password(newpwd))
        messages.success(request,"Password changed")
        logout(request)
        return redirect('/login/')
    return render(request,'passwordmail.html',{'usernm':usr,})