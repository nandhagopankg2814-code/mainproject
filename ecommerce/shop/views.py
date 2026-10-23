from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category
from shop.forms import SignupForm,LoginForm
class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        context={'category':c}
        return render(request,'categories.html',context)

class ProductView(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'category':c}
        return render(request,'products.html',context)

from shop.models import Product
class ProductDetail(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'productdetail.html',context)


class Register(View):
    def get(self,request):
        form_instance=SignupForm()
        return render(request,'register.html',{'form':form_instance})
    def post(self,request):
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('shop:categories')


from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

class Userlogin(View):
    def get(self,request):
        form_instance=LoginForm(request.POST)
        return render(request,'login.html',{'form':form_instance})

    def post(self,request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            name=form_instance.cleaned_data['username']
            pwd=form_instance.cleaned_data['password']
            user=authenticate(username=name,password=pwd) # return user object if entered username and password are correct
            if user and user.is_superuser==True:
                login(request,user) # starts a new session with current user
                return redirect('shop:categories')
            elif user and user.is_superuser==False:
                login(request, user)  # starts a new session with current user
                return redirect('shop:categories')
            else:  # if user does not exist
                # print("Invalid Credentials")
                messages.error(request,'Invalid Credentials, Please Enter Valid Username and Password')
                return render(request, 'login.html',{'form':form_instance})


class Userlogout(View):
    def get(self,request):
        logout(request) # removes user from the current session
        return redirect('shop:categories')

from shop.forms import CategoryForm,ProductForm

class AddCategory(View):
    def get(self, request):
        form_instance = CategoryForm()
        return render(request, 'addcategory.html', {'form': form_instance})

    def post(self, request):
        form_instance = CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('shop:categories')

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class AddProduct(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form_instance = ProductForm()
        return render(request, 'addproduct.html', {'form': form_instance})

    def post(self, request):
        form_instance = ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('shop:categories')

from shop.forms import StockForm
class AddStock(View):
    def get(self, request,i):
        p=Product.objects.get(id=i)
        form_instance = StockForm(instance=p)
        return render(request, 'addstock.html', {'form': form_instance})

    def post(self, request,i):
        p = Product.objects.get(id=i)
        form_instance = StockForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')