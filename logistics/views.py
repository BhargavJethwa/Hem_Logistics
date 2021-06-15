from logistics.forms import DriverForm,Trip_detailForm, VehicleForm,Bank_detailForm,ClientForm
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Bank_detail, Driver,Vehicle,Trip_detail,Client
from .helper_functions import check_expiry_insurance,check_expiry_license,check_expiry_PUC
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from pprint import pprint

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
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Driver")
	return render(request,'edit_driver.html', {'title':'Update Driver Details', 'form':form, 'driver':driver})
			
def delete_driver(request,id):
	driver = Driver.objects.get(id=id)
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
	trip = Trip_detail.objects.get(id=id)
	form = Trip_detailForm(request.POST, instance=trip)
	if form.is_valid():
		trip.Client=Client.objects.get(id=request.POST.get('Client'))
		trip.Driver=Driver.objects.get(id=request.POST.get('Driver'))
		trip.Vehicle=Vehicle.objects.get(id=request.POST.get('Vehicle'))
		trip.Bank_detail=Bank_detail.objects.get(id=request.POST.get('Bank_detail'))
		trip.Trip_id=request.POST.get('Trip_id')
		trip.Rate_type=request.POST.get('Rate_type')
		trip.Distance=request.POST.get('Distance')
		if request.POST.get('Rate') != '':
			trip.Rate=request.POST.get('Rate')
		else:
			trip.Rate=0
		trip.Freight=request.POST.get('Freight')
		trip.Advance_payment=request.POST.get('Advance_payment')
		trip.Source=request.POST.get('Source')
		i=1
		Destination=[]
		load_unload_charges=[request.POST.get('source_load_unload')]
		other_charges=[request.POST.get('source_other_charge')]
		total_payment=int(trip.Freight)+int(load_unload_charges[0])+int(other_charges[0])
		while(request.POST.get('destination_'+str(i)) is not None):
			Destination.append(request.POST.get('destination_'+str(i)))
			load_unload_charges.append(request.POST.get('destination_'+str(i)+'_load_unload'))
			other_charges.append(request.POST.get('destination_'+str(i)+'_other_charges'))
			total_payment = total_payment+int(load_unload_charges[i])+int(other_charges[i])
			i=i+1
		trip.Destination=json.dumps(Destination)
		trip.Load_unload_charges=json.dumps(load_unload_charges)
		trip.Other_charges=json.dumps(other_charges)
		trip.Total_payment = total_payment
		
		trip.save()			
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Trip Detail")
	return render(request,'edit_trip_detail.html', {'title':'Update Trip Details', 'form':form,'trip_detail':trip})
	
def delete_trip_detail(request,id):
	trip_detail = Trip_detail.objects.get(id=id)
	trip_detail.delete()
	return redirect("/Trip Detail")

def finish_trip_detail(request,id):
	trip_detail = Trip_detail.objects.get(id=id)
	trip_detail.Finished=True
	trip_detail.save()
	return redirect("/Trip Detail")

def trip_detail(request):						
	form = Trip_detailForm()
	if request.method=='POST':
		form = Trip_detailForm(request.POST)
		if form.is_valid():
			# pprint(request.POST)
			# form.save()
			trip=Trip_detail()
			trip.Client=Client.objects.get(id=request.POST.get('Client'))
			trip.Driver=Driver.objects.get(id=request.POST.get('Driver'))
			trip.Vehicle=Vehicle.objects.get(id=request.POST.get('Vehicle'))
			trip.Bank_detail=Bank_detail.objects.get(id=request.POST.get('Bank_detail'))
			trip.Trip_id=request.POST.get('Trip_id')
			trip.Rate_type=request.POST.get('Rate_type')
			trip.Distance=request.POST.get('Distance')
			if request.POST.get('Rate') != '':
				trip.Rate=request.POST.get('Rate')
			else:
				trip.Rate=0
			trip.Freight=request.POST.get('Freight')
			trip.Advance_payment=request.POST.get('Advance_payment')
			trip.Source=request.POST.get('Source')
			i=1
			Destination=[]
			load_unload_charges=[request.POST.get('source_load_unload')]
			other_charges=[request.POST.get('source_other_charge')]
			total_payment=int(trip.Freight)+int(load_unload_charges[0])+int(other_charges[0])
			while(request.POST.get('destination_'+str(i)) is not None):
				Destination.append(request.POST.get('destination_'+str(i)))
				load_unload_charges.append(request.POST.get('destination_'+str(i)+'_load_unload'))
				other_charges.append(request.POST.get('destination_'+str(i)+'_other_charges'))
				total_payment = total_payment+int(load_unload_charges[i])+int(other_charges[i])
				i=i+1
			trip.Destination=json.dumps(Destination)
			trip.Load_unload_charges=json.dumps(load_unload_charges)
			trip.Other_charges=json.dumps(other_charges)
			trip.Total_payment = total_payment
			
			trip.save()			
			messages.success(request, 'Added successfully!!!')
			form = Trip_detailForm()
			return redirect("/Trip Detail")

	return render(request, 'trip_detail.html', {'form': form, 'title':'Add Trip Detail'})

#################### Ajax for trip detail ####################################### 

def favorite_ajax(request):

	if request.method=='POST':
		driver_id=request.POST['driver_id']
		vehicle_id=request.POST['vehicle_id']
		if driver_id:
			driver = Driver.objects.get(id=driver_id)
			data=[]
			# print(type(driver))
			# print(type(driver.Vehicle.all()))
			for x in driver.Vehicle.all():
				data.append(x)
			
			data1 = serializers.serialize('json',driver.Vehicle.all())
			obj = json.loads(data1)

		if vehicle_id:
			vehicle=Vehicle.objects.get(id=vehicle_id)
			Banks = Bank_detail.objects.filter(Vehicle=vehicle)
			# print(type(Banks))

			
			data1 = serializers.serialize('json',Banks)
			obj = json.loads(data1)

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
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Vehicle")
	return render(request,'edit_vehicle.html', {'title':'Update Vehicle Details', 'form':form, 'vehicle':vehicle})
			
def delete_vehicle(request,id):
	vehicle = Vehicle.objects.get(id=id)
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
	return render(request, 'show_bank_detail.html', {'title':'Bank Detail', 'bank_detail':bank_detail })

def edit_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id) 
	form = Bank_detailForm(instance=bank_detail) 
	return render(request,'edit_bank_detail.html', {'title':'Update Bank Details', 'form':form, 'bank_detail':bank_detail})

def update_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id)
	form = Bank_detailForm(request.POST, instance=bank_detail)
	if form.is_valid():
		form.save()
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Bank Detail")
	return render(request,'edit_bank_detail.html', {'title':'Update Bank Details', 'form':form, 'bank_detail':bank_detail})
			
def delete_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id)
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

################ Client ################################################### 

def show_client(request):
	client = Client.objects.all()
	return render(request, 'show_client.html', {'title':'Client', 'client':client })

def edit_client(request,id):
	client = Client.objects.get(id=id) 
	form = ClientForm(instance=client) 
	return render(request,'edit_client.html', {'title':'Update Client', 'form':form, 'client':client})

def update_client(request,id):
	client = Client.objects.get(id=id)
	form = ClientForm(request.POST, instance=client)
	if form.is_valid():
		form.save()
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Client")
	return render(request,'edit_client.html', {'title':'Update client', 'form':form, 'client':client})
			
def delete_client(request,id):
	client = Client.objects.get(id=id)
	client.delete()
	return redirect("/Client")

def client(request):
	form = ClientForm()
	if request.method=='POST':
		form = ClientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Added successfully!!!')
			form = ClientForm()
			return redirect("/Client")

	return render(request, 'client.html', {'form': form, 'title':'Add Client'})

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

def PUC_notifications(request):
	check_expiry_PUC()
	PUC = Vehicle.objects.filter(PUC_expired=True)
	return render(request,'PUC_notifications.html',{'title':'Notifications', 'PUC':PUC})

def license_notifications(request):
	check_expiry_license()
	license = Driver.objects.filter(License_expired=True)
	return render(request,'license_notifications.html',{'title':'Notifications', 'license':license})

def insurance_notifications(request):
	check_expiry_insurance()
	insurance = Vehicle.objects.filter(Insurance_expired=True)
	return render(request,'insurance_notifications.html',{'title':'Notifications', 'insurance':insurance})
