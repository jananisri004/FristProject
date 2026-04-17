from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Count
from django.contrib import messages
import random

from .models import DecorPlan, Booking, UserOTP, Wishlist, Rating, PlanImage
from .forms import RegisterForm, BookingForm


# 🔐 USER LOGIN
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Find user by email
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()  # Get the first matching user
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('plans')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'User not found')
    
    return render(request, 'Event/user_login.html')


# 🔐 ADMIN LOGIN
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Find user by email
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()  # Get the first matching user
            
            # Authenticate first
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                # Check if user is staff after authentication
                if not user.is_staff:
                    messages.error(request, 'Access denied. This account is not authorized for admin access.')
                    return render(request, 'Event/admin_login.html')
                
                login(request, user)
                messages.success(request, f'Welcome Admin {user.first_name or user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Admin account not found')
    
    return render(request, 'Event/admin_login.html')


@login_required
def add_event(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to add events")
        return redirect('plans')
    
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            
            if not all([name, description, price, image]):
                messages.error(request, "All fields are required")
                all_plans = DecorPlan.objects.all()
                return render(request, 'Event/add_event.html', {'all_plans': all_plans})
            
            DecorPlan.objects.create(
                name=name,
                description=description,
                price=int(price),
                image=image
            )
            messages.success(request, "Event added successfully! ✅")
            return redirect('admin_events')
        except Exception as e:
            messages.error(request, f"Error adding event: {str(e)}")
            all_plans = DecorPlan.objects.all()
            return render(request, 'Event/add_event.html', {'all_plans': all_plans})
    
    all_plans = DecorPlan.objects.all()
    return render(request, 'Event/add_event.html', {'all_plans': all_plans})
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            request.session['user_id'] = user.id

            otp = random.randint(1000, 9999)
            UserOTP.objects.create(user=user, otp=otp)

            send_mail(
                "Your OTP Code",
                f"Your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect('verify_otp')

    return render(request, 'Event/register.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('register')

        user = User.objects.filter(id=user_id).first()
        user_otp = UserOTP.objects.filter(user=user, otp=otp).last()

        if user_otp:
            user.is_active = True
            user.save()

            user_otp.delete()
            del request.session['user_id']

            return redirect('login')
        else:
            return render(request, 'Event/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'Event/verify_otp.html')
# ── In your Event/views.py ──
# Replace your existing detail view with this:

def detail(request, id):
    plan = get_object_or_404(DecorPlan, id=id)

    # Get similar plans (same category, excluding current)
    similar_plans = DecorPlan.objects.exclude(id=id)[:3]

    return render(request, 'Event/detial.html', {
        'plan': plan,
        'similar_plans': similar_plans,
    })


# 🏠 PLANS (SEARCH + FILTER + RATING)
@login_required
def plans(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    decor_plans = DecorPlan.objects.annotate(
        avg_rating=Avg('rating__rating')
    )

    # 🔍 Search
    if query:
        decor_plans = decor_plans.filter(name__icontains=query)

    # 💰 Min price
    if min_price:
        try:
            decor_plans = decor_plans.filter(price__gte=float(min_price))
        except ValueError:
            pass

    # 💰 Max price
    if max_price:
        try:
            decor_plans = decor_plans.filter(price__lte=float(max_price))
        except ValueError:
            pass

    decor_plans = decor_plans.order_by('-id')

    return render(request, 'Event/plans.html', {'plans': decor_plans})


# 📅 BOOK EVENT
@login_required
def book(request, id):
    plan = get_object_or_404(DecorPlan, id=id)
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.decor_plan = plan
            booking.save()

            send_mail(
                "Booking Confirmation 🎉",
                f"Your booking for {plan.name} is confirmed!",
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )

            return redirect('my_bookings')

    return render(request, 'Event/booking.html', {
        'form': form,
        'plan': plan
    })


# 📋 MY BOOKINGS
@login_required
def my_bookings(request):
    data = Booking.objects.filter(user=request.user)
    return render(request, 'Event/my_bookings.html', {'data': data})


# 🔍 PLAN DETAIL
@login_required
def plan_detail(request, id):
    plan = get_object_or_404(DecorPlan, id=id)
    return render(request, 'Event/detail.html', {'plan': plan})


# ❤️ ADD TO WISHLIST
@login_required
def wishlist_add(request, id):
    plan = get_object_or_404(DecorPlan, id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, plan=plan)
    
    if created:
        messages.success(request, f"Added {plan.name} to wishlist! ❤️")
    else:
        messages.info(request, f"{plan.name} is already in your wishlist")
    
    return redirect('plan_detail', id=id)


# ❤️ REMOVE FROM WISHLIST
@login_required
def wishlist_remove(request, id):
    plan = get_object_or_404(DecorPlan, id=id)
    Wishlist.objects.filter(user=request.user, plan=plan).delete()
    messages.success(request, f"Removed {plan.name} from wishlist")
    return redirect('wishlist')


# ❤️ VIEW WISHLIST
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('plan')
    return render(request, 'Event/wishlist.html', {'wishlist_items': wishlist_items})


# 🗑️ DELETE EVENT
@login_required
def delete_event(request, id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete events")
        return redirect('plans')
    
    plan = get_object_or_404(DecorPlan, id=id)
    plan_name = plan.name
    plan.delete()
    messages.success(request, f"Event '{plan_name}' deleted successfully ✅")
    return redirect('admin_events')


# 📊 ADMIN DASHBOARD
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('plans')

    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    total_plans = DecorPlan.objects.count()

    popular = DecorPlan.objects.annotate(
        total_bookings=Count('booking')
    ).order_by('-total_bookings')[:5]

    recent_bookings = Booking.objects.select_related('user', 'decor_plan').order_by('-event_date')[:6]
    all_plans = DecorPlan.objects.all()[:6]

    return render(request, 'Event/admin/dashboard.html', {
        'users': total_users,
        'bookings': total_bookings,
        'plans': total_plans,
        'popular': popular,
        'recent_bookings': recent_bookings,
        'all_plans': all_plans,
    })


# 👥 ADMIN - ALL USERS
@login_required
def admin_users(request):
    if not request.user.is_staff:
        return redirect('plans')
    
    users = User.objects.all()
    return render(request, 'Event/admin/users.html', {'users': users})


# 📋 ADMIN - ALL BOOKINGS
@login_required
def admin_bookings(request):
    if not request.user.is_staff:
        return redirect('plans')
    
    bookings = Booking.objects.select_related('user', 'decor_plan').order_by('-event_date')
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    return render(request, 'Event/admin/bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter,
        'statuses': Booking.STATUS_CHOICES
    })


# 🚮 ADMIN - ALL EVENTS
@login_required
def admin_events(request):
    if not request.user.is_staff:
        return redirect('plans')
    
    plans = DecorPlan.objects.all()
    return render(request, 'Event/admin/events.html', {'plans': plans})


# ✏️ UPDATE BOOKING STATUS
@login_required
def update_booking_status(request, id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to update bookings")
        return redirect('plans')
    
    booking = get_object_or_404(Booking, id=id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Booking.STATUS_CHOICES):
        booking.status = new_status
        booking.save()
        messages.success(request, f"Booking status updated to {new_status} ✅")
    
    return redirect('admin_bookings')
@login_required
def add_wishlist(request, id):
    plan = get_object_or_404(DecorPlan, id=id)
    Wishlist.objects.get_or_create(user=request.user, plan=plan)
    return redirect('wishlist')
@login_required
def remove_wishlist(request, id):
    plan = get_object_or_404(DecorPlan, id=id)
    Wishlist.objects.filter(user=request.user, plan=plan).delete()
    return redirect('wishlist')