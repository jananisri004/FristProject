from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class DecorPlan(models.Model):
    """Event/Decoration Plan - can be added via Django Admin or the Add Event form"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Booking(models.Model):
    """Booking for a DecorPlan"""
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_IN_PROGRESS = 'in_progress'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_IN_PROGRESS, 'In Progress'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decor_plan = models.ForeignKey(DecorPlan, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    event_date = models.DateField()
    requirements = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return f"{self.user.username} - {self.decor_plan.name}"


# 🔐 OTP Verification
class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} OTP"


# ❤️ Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(DecorPlan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ❤️ {self.plan.name}"


# ⭐ Rating
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(DecorPlan, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} ⭐ {self.plan.name}"


class PlanImage(models.Model):
    plan = models.ForeignKey(DecorPlan, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.plan.name} Image"
