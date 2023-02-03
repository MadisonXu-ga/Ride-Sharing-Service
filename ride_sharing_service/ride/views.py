from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.core.mail import send_mass_mail
from django.contrib.auth.decorators import login_required

import datetime

from .models import *

def sign_in(request):
    if(request.method=="POST"):
        email = request.POST.get("user_email")
        password = request.POST.get("user_password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        print(user)
        if user is not None and check_password(password, user.password):
            login(request, user)

            return render(request, 'ride_request.html', {'user': user})
        else:
            print("////")
            return render(request, 'sign_in.html', {'error': 'Email does not exist or password is incorrect!'})
    elif request.method=="GET":
        return render(request, 'sign_in.html')

def sign_up(request):
    if(request.method=="POST"):
        name = request.POST["user_name"]
        email = request.POST["user_email"]
        password = request.POST['user_password']
        password2 = request.POST['user_password2']
        if password == password2:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return render(request, 'sign_up.html', {'error': 'Email already in use'})
            else:
                # Create the user
                user = User(username=name, email=email)
                user.set_password(password)
                # user = User.objects.create_user(
                #     username=name,
                #     email=email,
                #     password=password
                # )
                user.save()

                ride_user = RideUser.objects.create(user_name=name, password=password, email=email)
                ride_user.save()

                return redirect('/sign_in')
        else:
            return render(request, 'sign_up.html', {'error': 'Passwords do not match'})
    elif(request.method=="GET"):
        return render(request, 'sign_up.html')

def sign_out(request):
    logout(request)
    return redirect('/sign_in')

@login_required
def request_ride(request):
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
    if(request.method=="POST"):
        user = request.user
        print(user.email)
        owner = RideUser.objects.get(email=user.email)
        print(owner.id)
        destination = request.POST['desination']
        arrival_time = request.POST['arrival_time']
        vehicle_type = request.POST['vehicle_type']
        num_pax_owner = request.POST['num_pax']
        special_info = request.POST['special_info']
        sharable_check = request.POST.get('sharable_check', False)

        num_pax_total = num_pax_owner
        
        ride = Ride(owner=owner, destination=destination, arrival_time=arrival_time, vehicle_type=vehicle_type, 
                    num_pax_owner=num_pax_owner, num_pax_total=num_pax_total, special_requests=special_info, is_sharable=sharable_check)
        ride.save()
        return render(request, 'ride_request.html', {'success_message': "Request submitted successfully!"})

    # elif(request.method=="GET"):
    return render(request, 'ride_request.html', {'now': now})

@login_required
def get_rides(request):
    owner = RideUser.objects.get(email=request.user.email)
    ride_records1 = Ride.objects.filter(owner=owner)
    ride_records2 = Ride.objects.filter(sharers__in=[owner])

    ride_records = ride_records1 | ride_records2
    if(request.method=="POST"):
        status =  request.POST.get('status')

        if(status=="all"):
            return render(request, 'ride_select.html', {'records': ride_records, 'option': "all"})
        ride_records = ride_records.filter(status=status)
        return render(request, 'ride_select.html', {'records': ride_records, 'option': status})
    
    return render(request, 'ride_select.html', {'records': ride_records})

@login_required
def ride_info(request):
    # owner = RideUser.objects.get(email=request.user.email)
    # min_ = datetime.datetime.now()
    ride_id = request.GET.get('ride_id')
    print(ride_id)
    ride_record = Ride.objects.get(id=ride_id)
    print(ride_record.arrival_time)
    return render(request, 'ride_info.html', {'ride_record': ride_record})

@login_required
def edit_ride(request):
    if request.method=="POST":
        ride_id = request.GET.get('ride_id')
        ride_record = Ride.objects.get(id=ride_id)
        print(ride_id)
        ride_record = Ride.objects.get(id=ride_id)

        new_destination = request.POST["destination"]
        new_arrival_time = request.POST["arrival_time"]
        new_vehicle_type = request.POST["vehicle_type"]
        new_num_pax_owner = request.POST["num_pax_owner"]
        new_special_info = request.POST.get("special_info")
        new_sharable_check = request.POST.get('sharable_check', False)

        ride_record.destination = new_destination
        ride_record.arrival_time = new_arrival_time
        ride_record.vehicle_type = new_vehicle_type
        ride_record.num_pax_total = ride_record.num_pax_total-ride_record.num_pax_owner+new_num_pax_owner
        ride_record.num_pax_owner = new_num_pax_owner
        ride_record.special_requests = new_special_info
        ride_record.is_sharable = new_sharable_check

        ride_record.save()

@login_required
def account_info(request):
    ride_user = RideUser.objects.get(email=request.user.email)
    is_driver = False
    driver = None
    if Driver.objects.filter(user=ride_user).exists():
        is_driver = True
        driver = Driver.objects.get(user=ride_user)

    print(is_driver)

    return render(request, 'account_info.html', {'ride_user': ride_user, 'is_driver': is_driver, 'driver': driver})

@login_required
def edit_account(request):
    if(request.method=="POST"):
        user = User.objects.get(email=request.user.email)
        ride_user = RideUser.objects.get(email=request.user.email)

        new_username = request.POST["username"]
        new_email = request.POST["email"]

        user.username = new_username
        user.email = new_email

        ride_user.user_name = new_username
        ride_user.email = new_email

        user.save()
        ride_user.save()

        return redirect('/account_info/')

    return render(request, 'account_edit.html')

@login_required
def edit_vehicle(request):
    if(request.method=="POST"):
        user = User.objects.get(email=request.user.email)
        ride_user = RideUser.objects.get(email=request.user.email)

        new_vehicle_type = request.POST["vehicle_type"]
        new_license_plate_number = request.POST["license_plate_number"]
        new_max_num_pax = request.POST["max_num_pax"]

        if not Driver.objects.filter(user=ride_user).exists():
            driver = Driver.objects.create(user=ride_user, vehicle_type=new_vehicle_type, license_plate_number=new_license_plate_number, max_num_pax=new_max_num_pax)
            driver.save()
            return redirect('/account_info/')

        driver = Driver.objects.get(user=ride_user)

        driver.vehicle_type = new_vehicle_type
        driver.license_plate_number = new_license_plate_number
        driver.max_num_pax = new_max_num_pax

        driver.save()
        return redirect('/account_info/')

    return render(request, 'vehicle_edit.html')

@login_required
def cancel_vehicle(request):
    ride_user = RideUser.objects.get(email=request.user.email)
    if request.method=="POST":
        print("cancel_vehicle")
        driver = Driver.objects.get(user=ride_user)
        driver.delete()

        return redirect('/account_info/')

@login_required
def search_joinable_rides(request):
    # ride_user = RideUser.objects.get(email=request.user.email)
    records = None
    num_pax_sharer = 0
    # other conditions!!!
    if request.method == "POST":
        ride_user = RideUser.objects.get(email=request.user.email)
        records = Ride.objects.filter(status="open", is_sharable=True).exclude(owner=ride_user)
        destination = request.POST["destination"]
        e_time = request.POST["earliest_arrival_time"]
        l_time = request.POST["latest_arrival_time"]
        # ???????? passenger num?????????????
        num_pax_sharer = request.POST["num_pax"]

        records = records.filter(destination=destination, arrival_time__gte=e_time, arrival_time__lte=l_time)
        # return render(request, 'ride_join.html', {'records': records})
    
    return render(request, 'ride_join.html', {'records': records, 'num_pax_sharer': num_pax_sharer})

@login_required
def join_ride(request):
    is_in = False
    ride_user = RideUser.objects.get(email=request.user.email)
    if request.method=="POST":
        ride_id = request.POST.get('ride_id')
        num_pax_sharer = request.POST.get('num_pax_sharer')
        print('post:???????')
        print(ride_id)
        print(num_pax_sharer)
        ride_record = Ride.objects.get(id=ride_id)
        is_in = (ride_user in ride_record.sharers.all())
        if 'quit_submit' in request.POST:
            ride_record.sharers.remove(ride_user)
            # update remain seats??? do I need to add a field to ride???
            data = ride_record.sharer_num
            data.pop(ride_user.user_name, None)
            ride_record.num_pax_total -= int(num_pax_sharer)
            ride_record.save()
            is_in = False
        elif 'join_submit' in request.POST:
            ride_record.sharers.add(ride_user)
            ride_record.sharer_num[ride_user.user_name] = num_pax_sharer
            ride_record.num_pax_total += int(num_pax_sharer)
            ride_record.save()
            is_in = True

    elif request.method=="GET":
        ride_id = request.GET.get('ride_id')
        num_pax_sharer = request.GET.get('num_pax_sharer')
        # print(ride_id)
        # print(num_pax_sharer)
        ride_record = Ride.objects.get(id=ride_id)
        is_in = (ride_user in ride_record.sharers.all())
    
    return render(request, 'ride_info_join.html', {'is_in': is_in, 'ride_record': ride_record, 'ride_id': ride_id, 'num_pax_sharer':num_pax_sharer})

@login_required
def search_ride_driver(request):
    ride_user = RideUser.objects.get(email=request.user.email)
    if not Driver.objects.filter(user=ride_user).exists():
        return redirect('/account_info/', {'message': "You are not a driver! You can register as a driver now!"})
    driver = Driver.objects.get(user=ride_user)
    ride_records = Ride.objects.filter(status="open").filter(num_pax_total__lte=driver.max_num_pax).filter(vehicle_type=driver.vehicle_type)
    # ?????????????????????????????
    # ride_records_no_text = ride_records1.filter(special_requests__isnull=True)
    # print(ride_records_no_text)
    # ride_records_match_text = ride_records1.filter(special_requests=driver.special_info)
    # ride_records = ride_records_no_text | ride_records_match_text
    
    return render(request, 'ride_search_driver.html', {'ride_records': ride_records})

@login_required
def deal_ride_driver(request):
    ride_record = None
    ride_user = RideUser.objects.get(email=request.user.email)
    driver = Driver.objects.get(user=ride_user)
    if request.method=="GET":
        ride_id = request.GET.get('ride_id')
        print(ride_id)
        ride_record = Ride.objects.get(id=ride_id)
    if request.method=="POST":
        ride_id = request.POST.get('ride_id')
        ride_record = Ride.objects.get(id=ride_id)
        if ride_record.status=="open":
            ride_record.status = "confirmed"
            ride_record.driver = driver

            to_emails = [sharer.email for sharer in ride_record.sharers.all()]
            to_emails.append(ride_record.owner.email)

            email_data = (
                ('Ride Status Updated!',
                'Your ride request has been confirmed!',
                'steak_123@outlook.com',
                to_emails),
                )

            send_mass_mail(email_data, fail_silently=False)
            
            print(ride_record.status)
            ride_record.save()
            return redirect('/search_ride_driver/')
    
    return render(request, 'ride_search_info_driver.html', {'ride_record': ride_record})

@login_required
def get_rides_driver(request):
    ride_user = RideUser.objects.get(email=request.user.email)
    if not Driver.objects.filter(user=ride_user).exists():
        return redirect('/account_info/', {'message': "You are not a driver! You can register as a driver now!"})
    
    driver = Driver.objects.get(user=ride_user)
    ride_records = Ride.objects.filter(driver=driver)
    print("records!!")
    print(ride_records)
    print(ride_records.first().status)

    return render(request, 'ride_driver.html', {'ride_records': ride_records})

@login_required
def complete_ride_driver(request):
    ride_record = None
    if request.method=="GET":
        ride_id = request.GET.get('ride_id')
        print(ride_id)
        ride_record = Ride.objects.get(id=ride_id)
    if request.method=="POST":
        ride_id = request.POST.get('ride_id')
        ride_record = Ride.objects.get(id=ride_id)
        if ride_record.status=="confirmed":
            ride_record.status = "complete"
            ride_record.save()
            return redirect('/get_rides_driver/')
    
    return render(request, 'ride_info_driver.html', {'ride_record': ride_record})