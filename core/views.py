import uuid
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView
from .forms import SignupForm, LoginForm, ContactForm, ProfileUpdateForm, AttendanceForm
from django.contrib import messages
from core.models import Allcourse, Register, Payments, Profile, Attendance
# below is sending mail import................
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


class Contact(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            # Emails sending starts from here
            fname = form.cleaned_data.get("username")
            femail = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("Phone_number")
            desc = form.cleaned_data.get("desc")

            from_email = settings.EMAIL_HOST_USER

            # Prepare the email messages
            email_message = (
                f'Email from {fname}',
                f'UserEmail: {femail}\nUserPhoneNumber: {phone}\n\nQUERY: {desc}',
                from_email,
                ['rockyhasan.bspi@gmail.com', 'rockyhasan6201@gmail.com']
            )

            email_client = (
                'Rocky Hasan Response',
                'Thanks For Reaching us\n\narkprocoder.tech\n9986786453\nrocky@procoder.tech',
                from_email,
                [femail]
            )

            messages.info(request, "Thanks For Reaching Us! We will get back to you soon....")
            return redirect('contact')  # Use the named URL instead of hardcoding the URL

        # If the form is not valid, re-render the form with the entered data and validation errors
        return render(request, 'contact.html', {'form': form})


def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login or register.')
        return redirect('/signin/')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance applied successfully...!!!')
        return redirect('/profile/')
    return render(request, 'attendance.html')


def courses(request):
    courses = Allcourse.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def course(request, id):
    course = Allcourse.objects.filter(courseName=id)
    return render(request, 'course.html', {'course': course})


def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login & Register to connect with us')
        return redirect('/signin')
    courses = Allcourse.objects.all()
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        fathername = request.POST.get('fathername')
        email = request.POST.get('email')
        phoneno = request.POST.get('phoneno')
        address = request.POST.get('address')
        street = request.POST.get('street')
        city = request.POST.get('city')
        designation = request.POST.get('designation')
        qualification = request.POST.get('qualification')
        cknowledge = request.POST.get('cknowledge')
        scourse = request.POST.get('scourse')
        chcourse = request.POST.get('chcourse')

        if scourse == chcourse:
            pass
        else:
            messages.warning(request, 'Please select a valid course')
            return redirect('/enroll')

        query = Register(
            first_name=fname,
            last_name=lname,
            fathers_name=fathername,
            Phone_number=phoneno,
            email=email,
            address=address,
            street=street,
            city=city,
            designation=designation,
            qualification=qualification,
            computer_knowledge=cknowledge,
            course=scourse
        )
        query.save()
        messages.success(request, 'Enrollment success')
        return redirect('/profile')

    return render(request, 'enroll.html', {'courses': courses})


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login & Register to connect with us')
        return redirect('/signin')

    currentuser = request.user
    details = Register.objects.filter(email=currentuser.email).first()  # Get the Register object for the current user

    payment = Payments.objects.all()  # Get payment records for the current user
    paymentstatus = ""
    amount = 0
    balance = 0

    for payment_record in payment:
        paymentstatus = payment_record.status
        amount = payment_record.amountPaid
        balance = payment_record.balance

    paymentstats = {'paymentstatus': paymentstatus, 'amount': amount, 'balance': balance}
    attendanceStats = Attendance.objects.all()
    context = {'details': details, 'status': paymentstats, 'attendanceStats': attendanceStats}

    return render(request, 'profile.html', context)

def profileupdate(request, id):
    data = Register.objects.get(candidateId=id)
    courses = Allcourse.objects.all()
    context = {'data': data, 'courses': courses}
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        fathername = request.POST.get('fathername')
        email = request.POST.get('email')
        phoneno = request.POST.get('phoneno')
        address = request.POST.get('address')
        street = request.POST.get('street')
        city = request.POST.get('city')
        designation = request.POST.get('designation')
        qualification = request.POST.get('qualification')
        cknowledge = request.POST.get('cknowledge')
        scourse = request.POST.get('scourse')

        edit = Register.objects.get(candidateId=id)
        edit.first_name = firstname,
        edit.last_name = lastname,
        edit.fathers_name = fathername,
        edit.Phone_number = phoneno,
        edit.email = email,
        edit.address = address,
        edit.street = street,
        edit.city = city,
        edit.designation = designation,
        edit.qualification = qualification,
        edit.computer_knowledge = cknowledge,
        edit.course = scourse
        edit.save()
        messages.info(request, 'Data Update successfully  ')
        return redirect('/profile/')
    return render(request, 'profileupdate.html', context)


def logout(request):
    return render(request, 'logout.html')


def reset_pass(request):
    return render(request, 'reset_pass.html')


def send_email_after_registrations(email, token):
    try:
        subject = 'Verify your account'
        message = f'Click on the link to verify account/http://127.0.0.1:8000/signup/{token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        return False
    return True


class Signup(CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('signup')
    flag = 0

    def form_valid(self, form):
        user_form = form.save()
        uid = str(uuid.uuid4())
        pro_obj = Profile(user=user_form, token=uid)
        pro_obj.save()
        send_email_after_registrations(user_form.email, uid)
        messages.success(self.request, 'To verify your account please check your email')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'form is invalid please check your input')
        return super().form_invalid(form)
