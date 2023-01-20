import string
from django.shortcuts import render,redirect,reverse
from hms_admin.models import Staff,Doctor
from .models import Patient
from hms_admin.models import Department
# Create your views here.
def home(request):
    return render(request,'common/homepage.html')

def user_type(request):
    return render(request,'common/user_type.html')    
 
def about(request):
    return render(request,'common/about.html')

def contact(request):
    return render(request,'common/contact.html')

def dept(request):
    departments = Department.objects.all()
    return render(request,'common/department.html',{'departments':departments,})

def service(request):
    return render(request,'common/service.html')


def patient_registration(request):

    error_msg = ''
    success_msg = ''
    if request.method == 'POST':

        name = request.POST['pat_name']
        address = request.POST['pat_address']
        age = request.POST['pat_age']
        blood_group = request.POST['blood_grp']
        contact = request.POST['pat_phno']
        dob = request.POST['pat_dob']
        gender = request.POST['gender']
        email = request.POST['pat_email']

        record_exist = Patient.objects.filter(email = email).exists()

        if not record_exist :
            if 'pic' in request.FILES : # here pic is the name attribute of fileuploader
                pic = request.FILES['pic']
        
                patient_record = Patient( patient_name = name ,email = email, address = address , age = age , blood_grp = blood_group , 
                phone = contact , dob = dob , gender = gender , pic = pic )
                
            else :

                patient_record = Patient( patient_name = name ,email = email, address = address , age = age , blood_grp = blood_group , 
                phone = contact , dob = dob , gender = gender )

            
            patient_record.save()
            success_msg = 'Record Added Succesfully'

        else:
            error_msg = 'Email Exists'
    return render(request,'common/patient_register.html', {'success_msg' : success_msg, 'error_msg' : error_msg})

def login(request):
    user_type = request.GET['user']
    msg = ''
    
    # if 'patient' in request.session :
    #     return redirect('patient:home')

    # if 'doctor' in request.session :
    #     return redirect('doctor:dr_home')

    # if 'staff' in request.session :
    #     return redirect('staff:staff_home') 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if user_type ==  'staff':
             
            try :
                staff = Staff.objects.get(mail = username, password = password)
                request.session['staff'] = staff.id
                return redirect('staff:staff_home')
            except :
                msg = 'Invalid Username Or Password'

        if user_type == 'doc':
             
            try :
                doctor = Doctor.objects.get(username = username, password = password)
                request.session['doctor'] = doctor.id
                return redirect('doctor:dr_home')
            except :
                msg = 'Invalid Username Or Password'
        
        if user_type == 'patient':
             
            try :
                patient = Patient.objects.get(email = username, phone = password)
                request.session['patient'] = patient.id
                return redirect('patient:home')
            #     if request.session['log'] == True :
            #         return redirect('patient:appointment_1')

            #     request.session['log'] = False
            #     return redirect('patient:home')
            # except Exception as e :
            #     print(e)
            except:
                msg = 'Invalid Username Or Password'

        
    return render(request,'common/login.html', {'error_msg' : msg})

def department_details(request,id):
    department = Department.objects.get(id = id)
    doctors = Doctor.objects.filter(department = id)
    return render(request,'common/department_details.html',{ 'department': department,'doctors' : doctors})

def doctor_details(request,id):
    doctor = Doctor.objects.get(id = id)
    return render(request,'common/doctor_details.html',{'doctor': doctor,})

def doctor(request):
    return render(request,'common/hms_doctor.html')


def make_appointment(request):
 
    if 'patient' in request.session:
        return redirect('patient:appointment_1') 

  
    request.session['log'] = True
    return redirect(reverse('common:login') + '?user=patient') 
    

