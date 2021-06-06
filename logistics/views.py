from logistics.forms import DriverForm,Trip_detailForm, VehicleForm,Bank_detailForm
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Bank_detail, Driver,Vehicle,Trip_detail
from .helper_functions import check_expiry
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json

# Create your views here.

#################### index ####################################### 
def index(request):
	return redirect('home')

def home(request): 
	return render(request, 'index.html', {'title':'Home'}) 

#################### contact us ####################################### 

def contact_us(request): 
	return render(request, 'contact_us.html', {'title':'Contact us'}) 

#################### Driver ####################################### 

def show_driver(request):
	driver = Driver.objects.order_by('Name')
	return render(request, 'show_driver.html', {'title':'Driver', 'driver':driver })

def edit_driver(request,id):
	driver = Driver.objects.get(id=id) 
	form = DriverForm(instance=driver) 
	return render(request,'edit_driver.html', {'title':'Update Driver Details', 'form':form, 'driver':driver})

def update_driver(request,id):
	driver = Driver.objects.get(id=id)
	form = DriverForm(request.POST, instance=driver)
	if form.is_valid():
		form.save()
		return redirect("/Driver")
	return render(request,'edit_driver.html', {'title':'Update Driver Details', 'form':form, 'driver':driver})
			
def delete_driver(request,id):
	driver = Driver.objects.filter(id=id)
	driver.delete()
	return redirect("/Driver")

def driver(request):
	form = DriverForm()
	if request.method=='POST':
		form = DriverForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Added successfully!!!')
			form = DriverForm()
			return redirect("/Driver")

	return render(request, 'driver.html', {'form': form, 'title':'Add Driver'})

#################### Trip_detail ####################################### 

def show_trip_detail(request):
	trip_detail = Trip_detail.objects.order_by('Date_created')

	return render(request, 'show_trip_detail.html', {'title':'Trip Detail', 'trip_detail':trip_detail })

def edit_trip_detail(request,id):
	trip_detail = Trip_detail.objects.get(id=id) 
	form = Trip_detailForm(instance=trip_detail) 
	return render(request,'edit_trip_detail.html', {'title':'Update Trip Detail', 'form':form,'trip_detail':trip_detail})

def update_trip_detail(request,id):
	trip_detail = Trip_detail.objects.get(id=id)
	form = Trip_detailForm(request.POST, instance=trip_detail)
	if form.is_valid():
		form.save()
		return redirect("/Trip Detail")
	return render(request,'edit_trip_detail.html', {'title':'Update Trip Details', 'form':form,'trip_detail':trip_detail})
			
def delete_trip_detail(request,id):
	trip_detail = Trip_detail.objects.filter(id=id)
	trip_detail.delete()
	return redirect("/Trip Detail")

def trip_detail(request):						
	form = Trip_detailForm()
	if request.method=='POST':
		form = Trip_detailForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Added successfully!!!')
			form = Trip_detailForm()
			return redirect("/Trip Detail")

	return render(request, 'trip_detail.html', {'form': form, 'title':'Add Trip Detail'})

#################### Ajax for trip detail ####################################### 

def favorite_ajax(request):
	response_dict= {
			'success': False,
	}
	if request.method=='POST':
		id=request.POST['id']
		driver = Driver.objects.get(id=id)
		data=[]
		print(type(driver))
		print(type(driver.Vehicle.all()))
		for x in driver.Vehicle.all():
			data.append(x)
		
		data1 = serializers.serialize('json',driver.Vehicle.all())
		obj = json.loads(data1)
		# response_dict['success']= True
		# json.dumps(response_dict, default=lambda o: o.__dict__, 
        #     sort_keys=True, indent=4)
		# response_dict['car']=data1
	# return HttpResponse((response_dict))#, mimetype='application/json')
	return JsonResponse(obj,status=200,safe=False)

#################### Vehicle ####################################### 

def show_vehicle(request):
	vehicle = Vehicle.objects.all()
	return render(request, 'show_vehicle.html', {'title':'Vehicle', 'vehicle':vehicle })

def edit_vehicle(request,id):
	vehicle = Vehicle.objects.get(id=id) 
	form = VehicleForm(instance=vehicle) 
	return render(request,'edit_vehicle.html', {'title':'Update Vehicle Details', 'form':form,'vehicle':vehicle})

def update_vehicle(request,id):
	vehicle = Vehicle.objects.get(id=id)
	form = VehicleForm(request.POST, instance=vehicle)
	if form.is_valid():
		form.save()
		return redirect("/Vehicle")
	return render(request,'edit_vehicle.html', {'title':'Update Vehicle Details', 'form':form, 'vehicle':vehicle})
			
def delete_vehicle(request,id):
	vehicle = Vehicle.objects.filter(id=id)
	vehicle.delete()
	return redirect("/Vehicle")

def vehicle(request):
	form = VehicleForm()
	if request.method=='POST':
		form = VehicleForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Added successfully!!!')
			form = VehicleForm()
			return redirect("/Vehicle")

	return render(request, 'vehicle.html', {'form': form, 'title':'Add Vehicle'})

#################### Bank Detail ####################################### 

def show_bank_detail(request):
	bank_detail = Bank_detail.objects.all()
	return render(request, 'show_bank_detail.html', {'title':'Driver', 'bank_detail':bank_detail })

def edit_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id) 
	form = Bank_detailForm(instance=bank_detail) 
	return render(request,'edit_bank_detail.html', {'title':'Update Bank Details', 'form':form, 'bank_detail':bank_detail})

def update_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id)
	form = Bank_detailForm(request.POST, instance=bank_detail)
	if form.is_valid():
		form.save()
		return redirect("/Bank Detail")
	return render(request,'edit_bank_detail.html', {'title':'Update Bank Details', 'form':form, 'bank_detail':bank_detail})
			
def delete_bank_detail(request,id):
	bank_detail = Bank_detail.objects.filter(id=id)
	bank_detail.delete()
	return redirect("/Bank Detail")

def bank_detail(request):
	form = Bank_detailForm()
	if request.method=='POST':
		form = Bank_detailForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Added successfully!!!')
			form = Bank_detailForm()
			return redirect("/Bank Detail")

	return render(request, 'bank_detail.html', {'form': form, 'title':'Add Bank Detail'})

################ login forms ################################################### 

def Login(request): 
	form = AuthenticationForm()
	if request.method == 'POST': 
		username = request.POST['username'] 
		password = request.POST['password'] 
		user = authenticate(request, username = username, password = password) 
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!') 
			return redirect('/Home/', {'title':'Home'})
		else: 
			messages.info(request, f'account does not exit plz sign up') 
	return render(request, 'login.html', {'title':'log in', 'form':form})


################ Notifications ################################################### 

def notifications(request):
	check_expiry()
	insurance = Vehicle.objects.filter(Insurance_expired=True)
	PUC = Vehicle.objects.filter(PUC_expired=True)
	license = Driver.objects.filter(License_expired=True)
	return render(request,'notifications.html',{'title':'Notifications', 'PUC':PUC,'insurance':insurance,'license':license})