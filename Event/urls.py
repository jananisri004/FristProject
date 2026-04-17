from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.plans, name='plans'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user-login/', views.user_login, name='user_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    
    # Booking URLs
    path('book/<int:id>/', views.book, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    # Plan Details
    path('plan/<int:id>/', views.plan_detail, name='plan_detail'),
    path('detail/<int:id>/', views.detail, name='detail'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/remove/<int:id>/', views.wishlist_remove, name='wishlist_remove'),
    
    # Admin/Staff URLs
    path('staff/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/users/', views.admin_users, name='admin_users'),
    path('staff/bookings/', views.admin_bookings, name='admin_bookings'),
    path('staff/events/', views.admin_events, name='admin_events'),
    path('staff/booking/<int:id>/status/', views.update_booking_status, name='update_booking_status'),
    path('staff/add-event/', views.add_event, name='add_event'),
    path('staff/delete-event/<int:id>/', views.delete_event, name='delete_event'),
]

