from logistics.forms import DriverForm,Trip_detailForm,VehicleForm,Bank_detailForm
from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import Driver,Vehicle,Trip_detail

# Create your views here.

#################### index ####################################### 
def index(request):
    return redirect('home')

def home(request): 
	return render(request, 'index.html', {'title':'Home'}) 

#################### contact us ####################################### 

def contact_us(request): 
	return render(request, 'contact_us.html', {'title':'Contact us'}) 

def show_driver(request):
	drivers = Driver.objects.order_by('Name')
	return render(request, 'show_driver.html', {'title':'Driver', 'drivers':drivers })

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
	driver = Driver.objects.get(id=id)
	driver.delete()
	return redirect("/Driver")

def driver(request):
	form = DriverForm()
	if request.method=='POST':
		form = DriverForm(request.POST)
		# messages.add_message(request,messages.SUCCESS,'Added successfully')
		if form.is_valid():
			form.save()
			messages.add_message(request,messages.SUCCESS,'Added successfully')
			form = DriverForm()

	return render(request, 'driver.html', {'form': form, 'title':'Add Driver'})


def trip_detail(request):
	form = Trip_detailForm()
	if request.method=='POST':
		form = Trip_detailForm(request.POST)
		# messages.add_message(request,messages.SUCCESS,'Added successfully')
		if form.is_valid():
			# driver = Trip_detail()
			# driver.Name = request.POST['Name']
			# driver.License_number = request.POST['License_number']
			# driver.save()
			messages.add_message(request,messages.SUCCESS,'Added successfully')
			form = Trip_detailForm()

	return render(request, 'trip_detail.html', {'form': form, 'title':'Add Trip Detail'})


def vehicle(request):
	form = VehicleForm()
	if request.method=='POST':
		form = VehicleForm(request.POST)
		# messages.add_message(request,messages.SUCCESS,'Added successfully')
		if form.is_valid():
			# driver = Vehicle()
			# driver.Name = request.POST['Name']
			# driver.License_number = request.POST['License_number']
			# driver.save()
			messages.add_message(request,messages.SUCCESS,'Added successfully')
			form = VehicleForm()

	return render(request, 'vehicle.html', {'form': form, 'title':'Add Vehicle'})


def bank_detail(request):
	form = Bank_detailForm()
	if request.method=='POST':
		form = Bank_detailForm(request.POST)
		# messages.add_message(request,messages.SUCCESS,'Added successfully')
		if form.is_valid():
			# driver = Bank_detail()
			# driver.Name = request.POST['Name']
			# driver.License_number = request.POST['License_number']
			# driver.save()
			messages.add_message(request,messages.SUCCESS,'Added successfully')
			form = Bank_detailForm()

	return render(request, 'bank_detail.html', {'form': form, 'title':'Add Bank Detail'})