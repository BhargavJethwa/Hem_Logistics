from .models import Vehicle,Driver,Trip_detail
from django.utils.timezone import now
from datetime import timedelta,datetime
import json
import pandas as pd

def check_expiry_PUC():
    vehicles = Vehicle.objects.all()

    for vehicle in vehicles:
        if(vehicle.Notifications):
            if (vehicle.PUC_expiry_date - now().date())<timedelta(days=15):
                vehicle.PUC_expired=True
        else:
            vehicle.PUC_expired=False
        
        vehicle.save()

def check_expiry_insurance():
    vehicles = Vehicle.objects.all()
   
    for vehicle in vehicles:
        if(vehicle.Notifications):
            if (vehicle.Insurance_expiry_date - now().date())<timedelta(days=15):
                vehicle.Insurance_expired=True
        else:
            vehicle.Insurance_expired=False
        vehicle.save()

def check_expiry_license():
    drivers = Driver.objects.all()
    for driver in drivers:
        if (driver.License_expiry - now().date())<timedelta(days=15):
            driver.License_expired=True
        else:
            driver.License_expired=False
        driver.save()

def generate_trip_report(time_type,date1,date2):
    filename = "temp.xlsx"
    
    if(time_type=="daily"):
        ini = datetime.strptime(date1, '%Y-%m-%d')
        trips=Trip_detail.objects.filter(Date_created=ini)
        filename = "Trip_report-"+ini.strftime("%d-%m-%Y")+".xlsx"

    elif(time_type=="month"):
        ini=datetime.strptime(date1, '%Y-%m')
        trips=Trip_detail.objects.filter(Date_created__month=ini.month).filter(Date_created__year=ini.year)
        filename = "Trip_report-"+ini.strftime("%m-%Y")+".xlsx"
    
    elif(time_type=="period"):
        ini = datetime.strptime(date1, '%Y-%m-%d')
        end = datetime.strptime(date2, '%Y-%m-%d')
        trips=Trip_detail.objects.filter(Date_created__gte=ini).filter(Date_created__lte=end)
        filename = "Trip_report-"+ini.strftime("%d-%m-%Y")+" to "+end.strftime("%d-%m-%Y")+".xlsx"

    print(filename)

    # 'Date', 'Client', 'RC Number', 'Driver', 'Rate', 'Distance', 'Freight', 'Path', 'U/L', 'Other', 'Advance', 'Total'

    Date=[]
    Client=[]
    RC=[]
    Driver=[]
    Rate=[]
    Distance=[]
    Freight=[]
    Path=[]
    Unload_load=[]
    Other=[]
    Advance=[]
    Total=[]
    # writing the fields 
    for trip in trips:
        Date.append(trip.Date_created.strftime("%d/%m/%Y"))
        Client.append(trip.Client)
        RC.append(trip.Vehicle)
        Driver.append(trip.Driver)
        if(trip.Rate_type=="FIX"):
            Rate.append(trip.Rate_type)
        else:
            Rate.append(trip.Rate)
        Distance.append(str(trip.Distance)+" Km")
        Freight.append(trip.Freight)

        path=""
        path+=trip.Source+"\n"
        UL=""
        other=""
        dest=json.loads(trip.Destination)
        lu=json.loads(trip.Load_unload_charges)
        oth=json.loads(trip.Other_charges)
        for i in dest:
            path+=i+"\n"
        for i in lu:
            UL+=i+"\n"
        for i in oth:
            other+=i+"\n"
        path=path[:-1]
        UL=UL[:-1]
        other=other[:-1]

        Path.append(path)
        Unload_load.append(UL)
        Other.append(other)
        Advance.append(trip.Advance_payment)
        Total.append(trip.Total_payment)
        
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame({'Date':Date, 'Client':Client, 'RC Number':RC, 'Driver':Driver, 'Rate':Rate, 'Distance':Distance, 'Freight':Freight, 'Path':Path, 'U/L':Unload_load, 'Other':Other, 'Advance':Advance, 'Total':Total})
    df=df.set_index('Date')
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    return filename


def Vehicle_report(vehicle,month):
    ini=datetime.strptime(month, '%Y-%m')
    v = Vehicle.objects.get(id=vehicle)
    trips=Trip_detail.objects.filter(Date_created__month=ini.month).filter(Date_created__year=ini.year).filter(Vehicle=v)
    
    filename = "Vehicle_report-"+ini.strftime("%m-%Y")+".xlsx"
    print(filename)

    # 'Date', 'Client', 'RC Number', 'Driver', 'Rate', 'Distance', 'Freight', 'Path', 'U/L', 'Other', 'Advance', 'Total'

    Date=[]
    Client=[]
    RC=[]
    Driver=[]
    Rate=[]
    Distance=[]
    Freight=[]
    Path=[]
    Unload_load=[]
    Other=[]
    Advance=[]
    Total=[]
    # writing the fields 
    for trip in trips:
        Date.append(trip.Date_created.strftime("%d/%m/%Y"))
        Client.append(trip.Client)
        RC.append(trip.Vehicle)
        Driver.append(trip.Driver)
        if(trip.Rate_type=="FIX"):
            Rate.append(trip.Rate_type)
        else:
            Rate.append(trip.Rate)
        Distance.append(str(trip.Distance)+" Km")
        Freight.append(trip.Freight)

        path=""
        path+=trip.Source+"\n"
        UL=""
        other=""
        dest=json.loads(trip.Destination)
        lu=json.loads(trip.Load_unload_charges)
        oth=json.loads(trip.Other_charges)
        for i in dest:
            path+=i+"\n"
        for i in lu:
            UL+=i+"\n"
        for i in oth:
            other+=i+"\n"
        path=path[:-1]
        UL=UL[:-1]
        other=other[:-1]

        Path.append(path)
        Unload_load.append(UL)
        Other.append(other)
        Advance.append(trip.Advance_payment)
        Total.append(trip.Total_payment)
        
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame({'Date':Date, 'Client':Client, 'RC Number':RC, 'Driver':Driver, 'Rate':Rate, 'Distance':Distance, 'Freight':Freight, 'Path':Path, 'U/L':Unload_load, 'Other':Other, 'Advance':Advance, 'Total':Total})
    df=df.set_index('Date')
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    return filename