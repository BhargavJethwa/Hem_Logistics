from django.shortcuts import render, redirect 

# Create your views here.

#################### index ####################################### 
def index(request):
    return redirect('home')

def home(request): 
	return render(request, 'index.html', {'title':'Home'}) 

#################### contact us ####################################### 

def contact_us(request): 
	return render(request, 'contact_us.html', {'title':'Contact us'}) 