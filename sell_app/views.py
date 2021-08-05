import uuid


from . forms import (
    ProductForm, OrderForm,ProfileForm, UserForm
)
from . models import (
     Order, Products, Profile,User
)

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import (
    redirect, render,get_object_or_404
)
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
     CreateView, DeleteView
)



def home(request):
    products = Products.objects.all()
    item_name = request.GET.get('item_name')
   
    if item_name != '' and item_name is not None:
        products =products.filter(product_name__icontains = item_name)
    paginator = Paginator(products,4)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'sell_app/home.html', {'products':products})
    

def index(request):
    products = Products.objects.all()
    return render(request, 'sell_app/base.html',{'products':products})


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('sell_app/signup')
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token ,phone = phone)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)
    return render(request, 'sell_app/signup.html')


def userlogin(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')
        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('accounts/login')
        login(request , user)
        return redirect('home')
     return render(request, 'sell_app/login.html')


def success(request):
    return render(request , 'sell_app/success.html')


def token_send(request):
    return render(request , 'sell_app/token_send.html')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('sell_app/error')
    except Exception as e:
        print(e)
        return redirect('/') 


def error_page(request):
    return  render(request , 'sell_app/error.html')


class CreatePost( LoginRequiredMixin, CreateView ):
    form_class = ProductForm
    template_name = 'sell_app/create_post.html'
   
    def post(self, request):
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                products = form.save(commit=False)
                products.user_name = request.user
                products.save()
                return render(request, "sell_app/home.html")
        return redirect("home")
   

@login_required
def view_products(request):
    products = Products.objects.all()
    return render(request, 'sell_app/show_product.html', {'products': products})


@login_required
def product_desc(request, pk):
    products = Products.objects.get(pk=pk)
    form = OrderForm()
    seller = products.user_name
    products = Products.objects.get(pk=pk) 
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.seller = seller
            fm.buyer_name = request.user
            fm.item = products
            fm.order_status = False
            fm.save()
            subject = 'Sell-Buy'
            message = "Somebody has shown interest in your product"
            seller_email = seller.email
            send_mail(subject, 
            message, settings.EMAIL_HOST_USER, [seller_email], fail_silently = False)
            messages.success(request, 'Success!')
            return redirect('product_desc')
    return render(request, 'sell_app/product_desc.html', {'products': products, 'form':form})


@login_required
def my_posts(request):
    products = Products.objects.filter(user_name=request.user)
    return render(request, 'sell_app/product_details.html', {'products': products })


def editpost(request, pk):
    products = Products.objects.get(pk=pk)  
    form = ProductForm(instance=products)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance=products)
        if form.is_valid() :
            fm = form.save()
            fm.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'sell_app/edit_post.html', context)


class ProfileEditView(LoginRequiredMixin, CreateView):
    template_name= 'sell_app/edit_profile.html'
    form_class = ProfileForm
    
    def get(self, request):
        getdetails = Profile.objects.get(user = request.user)
        userform = UserForm(instance= request.user)
        detailsform = self.form_class( instance = getdetails)
        context = {'userform': userform, 'detailsform': detailsform}
        return render(request, self.template_name, context)

    def post(self, request):
        getdetails = Profile.objects.get(user = request.user)
        if request.method == 'POST':
            details_form = self.form_class(request.POST, request.FILES, instance = getdetails)
            userform = UserForm(request.POST, request.FILES, instance= request.user)
            if userform.is_valid():
                user = userform.save()
                user.save()
            if details_form.is_valid():
                details = details_form.save()
                details.save()
                messages.success(request, 'Profile details updated.')
                return redirect('home')
        else:
            userform = self.form_class(instance = request.user)
            details_form = self.form_class(instance = getdetails)       
        context = {'detailsform': details_form, 'userform': userform}
        return render(request, self.template_name, context)


class BuyProduct( LoginRequiredMixin, CreateView ):
    form_class = OrderForm
    template_name = 'sell_app/buy.html'

    def post(self, request):
        if request.method == 'POST':
            form = OrderForm(request.POST, request.FILES)
            def get(self,request,*args, **kwargs):
                users = User.objects.all()
                pro = Products.objects.product_name()
                args = {'users': users, 'pro':pro}
                return render(request, self.template_name, args)
            if form.is_valid():
                orders = form.save()
                orders.save()
                return render(request, "sell_app/buy.html")
        return redirect("home")


def view_buyers(request,pk):
    products = Products.objects.get(pk=pk)
    orders = Order.objects.filter(item = products)
    return render(request, 'sell_app/viewbuyers.html', {'orders' : orders})


def send_email(request, pk):
    orders = Order.objects.get(pk= pk)
    products = Products.objects.get(pk=orders.item.id)
    buyer = orders.buyer_name
    subject = 'Sell-Buy'
    message = "Somebody has shown interest in your product"
    buyer_email = buyer.email
    send_mail(subject, 
    message, settings.EMAIL_HOST_USER, [buyer_email], fail_silently = False)
    messages.success(request, 'Success!')
    return redirect('home')
    # return render(request, 'sell_app/viewbuyers.html', {'products': products, 'form':form})


class MyPost(LoginRequiredMixin,DetailView):
    model = Products
    template_name = 'sell_app/mypost.html'

    def get(self,request):
        products = Products.objects.filter()
        paginator = Paginator(products,4)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        return render(request,self.template_name,{'products':products})


def accept(request, pk):
    purchase = get_object_or_404(Order, pk=pk)
    purchase.order_status = True
    purchase.save(update_fields=['order_status'])
    return render(request,'sell_app/viewbuyers.html')

   
class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Products
    template_name = 'sell_app/delete_product.html'
    success_url = reverse_lazy('home')
 

class ViewPurchase(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'sell_app/viewpurchase.html'

    def get(self,request):
        orders = Order.objects.filter()
        paginator = Paginator(orders,4)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)
        return render(request,self.template_name,{'orders':orders})