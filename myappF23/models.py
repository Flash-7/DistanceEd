from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    STUDENT_STATUS_CHOICES = [
        ('ER', 'Enrolled'),
        ('SP', 'Suspended'),
        ('GD', 'Graduated'), ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES, default='enrolled')

    def __str__(self):
        return self.first_name + ", " + self.last_name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.first_name + ", " + self.last_name


class Course(models.Model):
    COURSE_LEVEL_CHOICES = [
        ("1", "Beginner"),
        ("2", "Intermediate"),
        ("3", "Advanced")
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructors = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=20, choices=COURSE_LEVEL_CHOICES)
    interested = models.PositiveIntegerField(default=0)
    interested_students = models.ManyToManyField(Student, blank=True, related_name='interested_students')

    def __str__(self):
        return self.title


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, "Order Confirmed"),
        (1, "Order Cancelled")
    ]
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField()
    order_price = models.DecimalField(decimal_places=2, max_digits=10)
    levels = models.PositiveIntegerField(default=1)

    def discount(self):
        discounted_price = float(self.courses.price) * 0.9
        self.order_price = discounted_price
        self.save()

    def save(self, *args, **kwargs):
        self.order_status = 0
        if self.order_price is None:
            self.order_price = self.courses.price
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return f"{self.students}'s order of {self.courses}"
