from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect
from django.views import View
from .models import CustomUser
from django.contrib import messages

class UserRegistrationView(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        my_location_link = request.POST.get('my_location_link')
        profile_picture = request.POST.get('profilepick')
        whatsapp_number = request.POST.get('whatsapp num')
        user = CustomUser(
            username = username,
            email =email,
            phone = phone,
            my_location_link =my_location_link,
            profile_picture =profile_picture,
            whatsapp_number =whatsapp_number
        )
        user.set_password(password)
        user.save()
        login(request,user)
        return redirect('home')
    
class UserLoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("hello",username,password)
        user = authenticate(request,username = username,password = password)
        print(user,"hello user")
        if user is not None:
            login(request,user)
            return redirect ('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
        
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html') 
    
class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('home')
