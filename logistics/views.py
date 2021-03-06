from logistics.forms import DriverForm, TransactionForm,Trip_detailForm, VehicleForm,Bank_detailForm,ClientForm
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Bank_detail, Driver, Transaction,Vehicle,Trip_detail,Client
from .helper_functions import Vehicle_report, check_expiry_insurance,check_expiry_license,check_expiry_PUC,generate_trip_report
from django.http import JsonResponse,HttpResponse
from django.core import serializers
import json,os,mimetypes

# Create your views here.

#################### index ####################################### 
@login_required(login_url='/login')
def index(request):
	return redirect('home')

@login_required(login_url='/login')
def home(request): 
	return render(request, 'index.html', {'title':'Home'}) 

#################### contact us ####################################### 
@login_required(login_url='/login')
def contact_us(request): 
	return render(request, 'contact_us.html', {'title':'Contact us'}) 

#################### Driver ####################################### 
@login_required(login_url='/login')
def show_driver(request):
	driver = Driver.objects.order_by('Name')
	return render(request, 'show_driver.html', {'title':'Driver', 'driver':driver })

@login_required(login_url='/login')
def edit_driver(request,id):
	driver = Driver.objects.get(id=id) 
	form = DriverForm(instance=driver) 
	return render(request,'edit_driver.html', {'title':'Update Driver Details', 'form':form, 'driver':driver})

@login_required(login_url='/login')
def update_driver(request,id):
	driver = Driver.objects.get(id=id)
	form = DriverForm(request.POST, instance=driver)
	if form.is_valid():
		form.save()
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Driver")
	return render(request,'edit_driver.html', {'title':'Update Driver Details', 'form':form, 'driver':driver})
			
@login_required(login_url='/login')
def delete_driver(request,id):
	driver = Driver.objects.get(id=id)
	try:
		driver.delete()
	except:
		messages.warning(request, 'Cannot be deleted!!! Please contact Admin')		
	return redirect("/Driver")

@login_required(login_url='/login')
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
@login_required(login_url='/login')
def show_trip_detail(request):
	trip_detail = Trip_detail.objects.order_by('Finished')

	return render(request, 'show_trip_detail.html', {'title':'Trip Detail', 'trip_detail':trip_detail })

@login_required(login_url='/login')
def edit_trip_detail(request,id):
	trip_detail = Trip_detail.objects.get(id=id) 
	form = Trip_detailForm(instance=trip_detail) 
	return render(request,'edit_trip_detail.html', {'title':'Update Trip Detail', 'form':form,'trip_detail':trip_detail})

@login_required(login_url='/login')
def update_trip_detail(request,id):
	trip = Trip_detail.objects.get(id=id)
	balance=int(trip.Advance_payment)
	form = Trip_detailForm(request.POST, instance=trip)
	if form.is_valid():
		transaction=Transaction.objects.get(Trip_detail=trip)
		trip.Client=Client.objects.get(id=request.POST.get('Client'))
		trip.Driver=Driver.objects.get(id=request.POST.get('Driver'))
		trip.Vehicle=Vehicle.objects.get(id=request.POST.get('Vehicle'))
		trip.Bank_detail=Bank_detail.objects.get(id=request.POST.get('Bank_detail'))
		trip.Trip_id=request.POST.get('Trip_id')
		trip.Rate_type=request.POST.get('Rate_type')
		trip.Distance=request.POST.get('Distance')
		if request.POST.get('Rate') != '':
			trip.Rate=request.POST.get('Rate')
			trip.Freight=int(trip.Distance)*int(trip.Rate)
		else:
			trip.Rate=0
			trip.Freight=request.POST.get('Freight')

		vehicle=Vehicle.objects.get(id=request.POST.get('Vehicle'))
		trip.Advance_payment=request.POST.get('Advance_payment')
		vehicle.Balance=vehicle.Balance+int(trip.Advance_payment)-balance
		transaction.Amount=trip.Advance_payment
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
	
		if(trip.Total_payment<int(trip.Advance_payment)):
				messages.warning(request, 'Advance cannot be greater than Total amount!!!')
				return render(request,'edit_trip_detail.html', {'title':'Update Trip Details', 'form':form,'trip_detail':trip})

		trip.save()				
		transaction.save()
		vehicle.save()
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Trip Detail")
	return render(request,'edit_trip_detail.html', {'title':'Update Trip Details', 'form':form,'trip_detail':trip})
	
@login_required(login_url='/login')
def delete_trip_detail(request,id):
	trip_detail = Trip_detail.objects.get(id=id)
	vehicle=trip_detail.Vehicle
	transaction=Transaction.objects.get(Trip_detail=trip_detail)

	vehicle.Balance=vehicle.Balance-int(trip_detail.Advance_payment)+int(trip_detail.Total_payment)
	vehicle.save()
	try:
		transaction.delete()
		trip_detail.delete()
	except:
		messages.warning(request, 'Cannot be deleted!!! Please contact Admin')	
	return redirect("/Trip Detail")

@login_required(login_url='/login')
def finish_trip_detail(request,id):
	trip_detail = Trip_detail.objects.get(id=id)
	trip_detail.Finished=True
	trip_detail.save()
	return redirect("/Trip Detail")

@login_required(login_url='/login')
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
				trip.Freight=int(trip.Distance)*int(trip.Rate)
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
				
			if(trip.Total_payment<int(trip.Advance_payment)):
				messages.warning(request, 'Advance cannot be greater than Total amount!!!')
				return render(request, 'trip_detail.html', {'form': form, 'title':'Add Trip Detail'})
				

			transaction=Transaction()
			transaction.Trip_detail=trip
			transaction.Vehicle=trip.Vehicle
			transaction.Bank_detail=trip.Bank_detail
			transaction.Amount=trip.Advance_payment
			transaction.Is_advance=True
			transaction.Details="Advance"
			
			vehicle=Vehicle.objects.get(id=request.POST.get('Vehicle'))
			vehicle.Balance = vehicle.Balance+int(trip.Advance_payment)-int(trip.Total_payment)

			trip.save()
			transaction.save()
			vehicle.save()

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

@login_required(login_url='/login')
def show_vehicle(request):
	vehicle = Vehicle.objects.all()
	return render(request, 'show_vehicle.html', {'title':'Vehicle', 'vehicle':vehicle })

@login_required(login_url='/login')
def edit_vehicle(request,id):
	vehicle = Vehicle.objects.get(id=id) 
	form = VehicleForm(instance=vehicle) 
	return render(request,'edit_vehicle.html', {'title':'Update Vehicle Details', 'form':form,'vehicle':vehicle})

@login_required(login_url='/login')
def update_vehicle(request,id):
	vehicle = Vehicle.objects.get(id=id)
	form = VehicleForm(request.POST, instance=vehicle)
	if form.is_valid():
		form.save()
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Vehicle")
	return render(request,'edit_vehicle.html', {'title':'Update Vehicle Details', 'form':form, 'vehicle':vehicle})
			
@login_required(login_url='/login')
def delete_vehicle(request,id):
	vehicle = Vehicle.objects.get(id=id)
	try:
		vehicle.delete()
	except:
		messages.warning(request, 'Cannot be deleted!!! Please contact Admin')
	return redirect("/Vehicle")

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def show_bank_detail(request):
	bank_detail = Bank_detail.objects.all()
	return render(request, 'show_bank_detail.html', {'title':'Bank Detail', 'bank_detail':bank_detail })

@login_required(login_url='/login')
def edit_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id) 
	form = Bank_detailForm(instance=bank_detail) 
	return render(request,'edit_bank_detail.html', {'title':'Update Bank Details', 'form':form, 'bank_detail':bank_detail})

@login_required(login_url='/login')
def update_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id)
	form = Bank_detailForm(request.POST, instance=bank_detail)
	if form.is_valid():
		form.save()
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Bank Detail")
	return render(request,'edit_bank_detail.html', {'title':'Update Bank Details', 'form':form, 'bank_detail':bank_detail})
			
@login_required(login_url='/login')
def delete_bank_detail(request,id):
	bank_detail = Bank_detail.objects.get(id=id)
	try:
		bank_detail.delete()
	except:
		messages.warning(request, 'Cannot be deleted!!! Please contact Admin')		
	return redirect("/Bank Detail")

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def show_client(request):
	client = Client.objects.all()
	return render(request, 'show_client.html', {'title':'Client', 'client':client })

@login_required(login_url='/login')
def edit_client(request,id):
	client = Client.objects.get(id=id) 
	form = ClientForm(instance=client) 
	return render(request,'edit_client.html', {'title':'Update Client', 'form':form, 'client':client})

@login_required(login_url='/login')
def update_client(request,id):
	client = Client.objects.get(id=id)
	form = ClientForm(request.POST, instance=client)
	if form.is_valid():
		form.save()
		messages.success(request, 'Updated successfully!!!')
		return redirect("/Client")
	return render(request,'edit_client.html', {'title':'Update Client', 'form':form, 'client':client})
			
@login_required(login_url='/login')
def delete_client(request,id):
	client = Client.objects.get(id=id)
	try:
		client.delete()
	except:
		messages.warning(request, 'Cannot be deleted!!! Please contact Admin')
	return redirect("/Client")

@login_required(login_url='/login')
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


################ Transaction ################################################### 

@login_required(login_url='/login')
def show_transaction(request):
	transaction = Transaction.objects.all()
	return render(request, 'show_transaction.html', {'title':'Transaction', 'transaction':transaction })

@login_required(login_url='/login')
def edit_transaction(request,id):
	transaction = Transaction.objects.get(id=id) 
	form = TransactionForm(instance=transaction) 
	return render(request,'edit_transaction.html', {'title':'Update Transaction', 'form':form, 'transaction':transaction})

@login_required(login_url='/login')
def update_transaction(request,id):
	transaction = Transaction.objects.get(id=id)
	balance = transaction.Amount
	vehicle=transaction.Vehicle
	form = TransactionForm(request.POST, instance=transaction)
	if form.is_valid():
		form.save()
		
		vehicle.Balance = vehicle.Balance+int(request.POST.get('Amount'))-int(balance)
		vehicle.save()

		messages.success(request, 'Updated successfully!!!')
		return redirect("/Transaction")
	return render(request,'edit_transaction.html', {'title':'Update Transaction', 'form':form, 'transaction':transaction})
			
@login_required(login_url='/login')
def delete_transaction(request,id):
	transaction = Transaction.objects.get(id=id)
	
	vehicle=transaction.Vehicle
	vehicle.Balance = vehicle.Balance-int(transaction.Amount)
	vehicle.save()
	
	try:
		transaction.delete()
	except:
		messages.warning(request, 'Cannot be deleted!!! Please contact Admin')
	return redirect("/Transaction")

@login_required(login_url='/login')
def transaction(request):
	form = TransactionForm()
	if request.method=='POST':
		form = TransactionForm(request.POST)
		if form.is_valid():
			form.save()
			vehicle=Vehicle.objects.get(id=request.POST.get('Vehicle'))
			vehicle.Balance = vehicle.Balance+int(request.POST.get('Amount'))
			vehicle.save()
			messages.success(request, 'Added successfully!!!')
			form = TransactionForm()
			return redirect("/Transaction")

	return render(request, 'transaction.html', {'form': form, 'title':'Add Transaction'})

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
			return redirect(request.POST.get('next'))
		else: 
			messages.info(request, f'account does not exit plz sign up') 
	return render(request, 'login.html', {'title':'log in', 'form':form})


################ Notifications ################################################### 

@login_required(login_url='/login')
def PUC_notifications(request):
	check_expiry_PUC()
	PUC = Vehicle.objects.filter(PUC_expired=True)
	return render(request,'PUC_notifications.html',{'title':'PUC', 'PUC':PUC})

@login_required(login_url='/login')
def license_notifications(request):
	check_expiry_license()
	license = Driver.objects.filter(License_expired=True)
	return render(request,'license_notifications.html',{'title':'License', 'license':license})

@login_required(login_url='/login')
def insurance_notifications(request):
	check_expiry_insurance()
	insurance = Vehicle.objects.filter(Insurance_expired=True)
	return render(request,'insurance_notifications.html',{'title':'Insurance', 'insurance':insurance})

################ File Download ################################################### 

@login_required(login_url='/login')
def report(request):
	vehicle=Vehicle.objects.all()
	return render(request,'generate_report.html',{'title':'Generate Report', 'vehicle' : vehicle})


################ File Download ################################################### 

@login_required(login_url='/login')
def generate_report(request):
	directory = "./"
	files_in_directory = os.listdir(directory)
	filtered_files = [file for file in files_in_directory if file.endswith(".xlsx")]
	for file in filtered_files:
		path_to_file = os.path.join(directory, file)
		os.remove(path_to_file)
	time_type=request.POST.get('time_type')
	date1=request.POST.get('date1')
	date2=request.POST.get('date2')
	name = generate_trip_report(time_type,date1,date2)
	fl = open(name, 'rb')
	mime_type, _ = mimetypes.guess_type(name)
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % name
	return response

@login_required(login_url='/login')
def vehicle_report(request):
	directory = "./"
	files_in_directory = os.listdir(directory)
	filtered_files = [file for file in files_in_directory if file.endswith(".xlsx")]
	for file in filtered_files:
		path_to_file = os.path.join(directory, file)
		os.remove(path_to_file)
	vehicle=request.POST.get('Vehicle')
	month=request.POST.get('month')
	name = Vehicle_report(vehicle,month)
	fl = open(name, 'rb')
	mime_type, _ = mimetypes.guess_type(name)
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % name
	return response