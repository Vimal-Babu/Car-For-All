from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect,get_object_or_404
from django.views import View
from .models import CustomUser,OilType,Brand,CarForSale,CarForRent
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
        list_all_car = CarForSale.objects.all() 
        list_my_cars = CarForSale.objects.filter(user=request.user) if request.user.is_authenticated else None
        all_rent_cars = CarForRent.objects.all()
        my_rent_cars = CarForRent.objects.filter(user =request.user) if request.user.is_authenticated else None
        context = {
        'list_all_car': list_all_car,
        'list_my_cars': list_my_cars,
        'all_rent_cars': all_rent_cars,
        'my_rent_cars': my_rent_cars
        }
        return render(request,'home.html',context)
    
class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('home')
    

class CarForSaleView(View):
    def get(self,request):
        brands = Brand.objects.all()
        print(brands,"brands")
        oil_type = OilType.objects.all()
        print(oil_type,"oil type")
        # for freeley rendering the page
        
        return render(request,'car_for_sale_form.html',{'brands':brands,'oil_types':oil_type})
    
    def post(self,request):
        # extrancting field and assign to values and save to the data base if all correct and ok sent to home page and show a mesage like 
        # sucss fulley added the car if any issues on the field showing error message
        name = request.POST.get('name')
        model_year = request.POST.get('model_year')
        km_driven = request.POST.get('km_driven')
        brand_id = request.POST.get('brand')
        oil_type_id = request.POST.get('oil_type')
        accidental_background = request.POST.get('accidental_background') == 'on'
        description = request.POST.get('description')
        price = request.POST.get('price')
        mileage = request.POST.get('mileage')
        registration_number = request.POST.get('registration_number')
        insurance_end_date = request.POST.get('insurance_end_date')
        ownership_type = request.POST.get('ownership_type')

        front_image = request.FILES.get('front_image')

        car_for_sale = CarForSale(
            user=request.user,
            name=name,
            modelYear=model_year,
            km_driven=km_driven,
            brand_id=brand_id,
            oil_type_id=oil_type_id,
            accidental_background=accidental_background,
            description=description,
            price=price,
            mileage=mileage,
            registration_number=registration_number,
            insurance_end_date=insurance_end_date,
            ownership_type=ownership_type,
            front_image=front_image,
        )

        car_for_sale.save()
        messages.success(request, 'Car for sale added successfully!')
        return redirect('home')
class CarForRentView(View):
    def get(self,request):
        brands = Brand.objects.all()
        oil_types = OilType.objects.all()
        context = {
            'brands':brands,
            'oil_types':oil_types
        }
        return render(request,'car_for_rent.html',context)
    def post(self,request):
        name = request.POST.get('name')
        brand_id = request.POST.get('brand') 
        oil_type_id = request.POST.get('oil_type')
        description = request.POST.get('description')
        price_per_day = request.POST.get('price_per_day')
        mileage = request.POST.get('mileage')
        rent_car_image = request.FILES.get('rent_car_image')

        # Validate and save the data
        if name and brand_id and oil_type_id and description and price_per_day and mileage:
            try:
                # Save car for rent to the database
                car_for_rent = CarForRent.objects.create(
                    user=request.user,
                    name=name,
                    brand_id=brand_id,
                    oil_type_id=oil_type_id,
                    description=description,
                    price_per_day=price_per_day,
                    mileage=mileage,
                    rent_car_image=rent_car_image
                )
                car_for_rent.save()
                messages.success(request, 'Car for rent added successfully!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Error saving car for rent: {e}")
        else:
            messages.error(request, "All fields are required.")

        # If there's an error, re-render the form with the original values and error message
        brands = Brand.objects.all()
        oil_types = OilType.objects.all()
        return render(request, 'car_for_rent.html', {'brands': brands, 'oil_types': oil_types})


class CarForSaleDetailView(View):
    def get(self, request):
        car_for_sale = CarForSale.objects.select_related('user').all()
        context = {
            'car_for_sale': car_for_sale
        }
        return render(request, 'car_for_sale_detail.html', context)

class CarForRentDetailView(View):
    def get(self, request):
        car_for_rent = CarForRent.objects.select_related('user').all()
        context = {
            'car_for_rent': car_for_rent
        }
        return render(request, 'car_for_rent_detail.html', context)


# class MyCarsForSaleView(View):
#     def get(self, request):
#         cars_for_sale = CarForSale.objects.filter(user=request.user)
#         return render(request, 'my_cars_for_sale.html', {'cars_for_sale': cars_for_sale})
    
class MyCarsForSaleView(View):
    def get(self, request):
        cars_for_sale = CarForSale.objects.filter(user=request.user)

        # Get filter parameters from the request
        brand_filter = request.GET.get('brand')
        year_filter = request.GET.get('year')
        price_filter = request.GET.get('price')
        search_query = request.GET.get('search')

        # Apply filters
        if brand_filter:
            cars_for_sale = cars_for_sale.filter(brand_id=brand_filter)

        if year_filter:
            # Filter based on model year (assuming modelYear is a field in your model)
            if year_filter == 'below_3':
                cars_for_sale = cars_for_sale.filter(modelYear__gte=2022)
            elif year_filter == '3_to_5':
                cars_for_sale = cars_for_sale.filter(modelYear__gte=2018, modelYear__lt=2022)
            elif year_filter == '5_to_10':
                cars_for_sale = cars_for_sale.filter(modelYear__gte=2013, modelYear__lt=2018)
            elif year_filter == 'above_10':
                cars_for_sale = cars_for_sale.filter(modelYear__lt=2013)

        if price_filter:
            if price_filter == 'below_50k':
                cars_for_sale = cars_for_sale.filter(price__lt=50000)
            elif price_filter == '1L_to_3L':
                cars_for_sale = cars_for_sale.filter(price__gte=50000, price__lt=300000)
            elif price_filter == '3L_to_5L':
                cars_for_sale = cars_for_sale.filter(price__gte=300000, price__lt=500000)
            elif price_filter == '5L_to_10L':
                cars_for_sale = cars_for_sale.filter(price__gte=500000, price__lt=1000000)
            elif price_filter == 'above_10L':
                cars_for_sale = cars_for_sale.filter(price__gte=1000000)

        if search_query:
            cars_for_sale = cars_for_sale.filter(name__icontains=search_query)

        # Fetch all brands for the filter dropdown
        brands = Brand.objects.all()

        return render(request, 'my_cars_for_sale.html', {
            'cars_for_sale': cars_for_sale,
            'brands': brands,
            'selected_brand': brand_filter,
            'selected_year': year_filter,
            'selected_price': price_filter,
            'search_query': search_query,
        })
# class MyCarsForRentView(View):
#     def get(self, request):
#         cars_for_rent = CarForRent.objects.filter(user=request.user)
#         return render(request, 'my_cars_for_rent.html', {'cars_for_rent': cars_for_rent})


class MyCarsForRentView(View):
    def get(self, request):
        cars_for_rent = CarForRent.objects.filter(user=request.user)
        print(cars_for_rent,"car for rentttttttttttttt")

        # Get filter parameters from the request
        brand_filter = request.GET.get('brand')
        print(brand_filter,"brand filtereeeeeeeee")
        year_filter = request.GET.get('year')
        print(year_filter)
        price_filter = request.GET.get('price')
        print(price_filter)
        search_query = request.GET.get('search')
        print(search_query,"serch keywordddd")

        # Apply filters
        if brand_filter:
            cars_for_rent = cars_for_rent.filter(brand_id=brand_filter)

        if year_filter:
            # Assuming modelYear is a field in your model
            if year_filter == 'below_3':
                cars_for_rent = cars_for_rent.filter(modelYear__gte=2022)
            elif year_filter == '3_to_5':
                cars_for_rent = cars_for_rent.filter(modelYear__gte=2018, modelYear__lt=2022)
            elif year_filter == '5_to_10':
                cars_for_rent = cars_for_rent.filter(modelYear__gte=2013, modelYear__lt=2018)
            elif year_filter == 'above_10':
                cars_for_rent = cars_for_rent.filter(modelYear__lt=2013)

        if price_filter:
            if price_filter == 'below_50':
                cars_for_rent = cars_for_rent.filter(price_per_day__lt=50)
            elif price_filter == '50_to_100':
                cars_for_rent = cars_for_rent.filter(price_per_day__gte=50, price_per_day__lt=100)
            elif price_filter == '100_to_200':
                cars_for_rent = cars_for_rent.filter(price_per_day__gte=100, price_per_day__lt=200)
            elif price_filter == '200_to_500':
                cars_for_rent = cars_for_rent.filter(price_per_day__gte=200, price_per_day__lt=500)
            elif price_filter == 'above_500':
                cars_for_rent = cars_for_rent.filter(price_per_day__gte=500)

        if search_query:
            cars_for_rent = cars_for_rent.filter(name__icontains=search_query)

        # Fetch all brands for the filter dropdown
        brands = Brand.objects.all()

        return render(request, 'my_cars_for_rent.html', {
            'cars_for_rent': cars_for_rent,
            'brands': brands,
            'selected_brand': brand_filter,
            'selected_year': year_filter,
            'selected_price': price_filter,
            'search_query': search_query,
        })




class EditCarForSaleView(View):
    def get(self, request, pk):
        print("edit car for sale workssssssssssss")
        print(request.user)
        car = get_object_or_404(CarForSale, pk=pk, user=request.user)
        print(car,"carrrrr")
        brands = Brand.objects.all()
        print(brands,"brandssssssssss")
        oil_types = OilType.objects.all()
        print(oil_types,"oil typeeeeeeeeeeeee")
        return render(request, 'edit_car_for_sale.html', {'car': car, 'brands': brands, 'oil_types': oil_types})

    def post(self, request, pk):
        car = get_object_or_404(CarForSale, pk=pk, user=request.user)
        # Update car details with form data
        car.name = request.POST.get('name')
        car.modelYear = request.POST.get('modelYear')
        car.km_driven = request.POST.get('km_driven')
        car.brand_id = request.POST.get('brand')
        car.oil_type_id = request.POST.get('oil_type')
        car.accidental_background = 'accidental_background' in request.POST
        car.description = request.POST.get('description')
        car.price = request.POST.get('price')
        car.mileage = request.POST.get('mileage')
        car.registration_number = request.POST.get('registration_number')
        car.insurance_end_date = request.POST.get('insurance_end_date')
        car.ownership_type = request.POST.get('ownership_type')
        car.save()
        return redirect('my_cars_for_sale')
    

class EditCarForRentView(View):
    def get(self, request, pk):
        car = get_object_or_404(CarForRent, pk=pk, user=request.user)
        brands = Brand.objects.all()  # Assuming you have a Brand model
        oil_types = OilType.objects.all()  # Assuming you have an OilType model
        return render(request, 'edit_car_for_rent.html', {'car': car, 'brands': brands, 'oil_types': oil_types})

    def post(self, request, pk):
        car = get_object_or_404(CarForRent, pk=pk, user=request.user)
        car.name = request.POST.get('name')
        car.brand_id = request.POST.get('brand')  # Set brand by ID
        car.oil_type_id = request.POST.get('oil_type')  # Set oil type by ID
        car.description = request.POST.get('description')
        car.price_per_day = request.POST.get('price_per_day')
        car.mileage = request.POST.get('mileage')

        if 'rent_car_image' in request.FILES:
            car.rent_car_image = request.FILES['rent_car_image']

        car.save()
        return redirect('my_cars_for_rent')



class DeleteCarForSaleView(View):
    def post(self, request, pk):
        car = get_object_or_404(CarForSale, pk=pk, user=request.user)
        car.delete()
        return redirect('my_cars_for_sale')
    

class DeleteCarForRentView(View):
    def post(self, request, pk):
        car = get_object_or_404(CarForRent, pk=pk, user=request.user)
        car.delete()
        return redirect('my_cars_for_rent')
    








# class ListAllCars(View):
#     def get(self, request):
#         list_all_car = CarForSale.objects.all()  
#         return render(request, 'index.html', {'all_cars': list_all_car})
# class ListMyCars(View):
#     def get(self,request):
#         list_my_cars = CarForSale.objects.filter(user = request.user)
#         return render(request, 'index.html', {'my_cars': list_my_cars})