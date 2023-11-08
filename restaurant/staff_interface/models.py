from django.db import models

from datetime import datetime, time

class OpeningHours(models.Model):
    class weekdays(models.IntegerChoices):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6
        
    DEFAULT_OPEN_TIME_RECURRING = time.fromisoformat("08:00:00")
    DEFAULT_CLOSE_TIME_RECURRING = time.fromisoformat("22:00:00")
    
    day = models.IntegerField(choices=weekdays.choices)
    open_time = models.TimeField(default=DEFAULT_OPEN_TIME_RECURRING)
    close_time = models.TimeField(default=DEFAULT_CLOSE_TIME_RECURRING)
    
    def __str__(self):
        return self.get_weekday_str() + ":\t " + (
            self.open_time.strftime("%H:%M") + " to " +
            self.close_time.strftime("%H:%M"))
        
        
    def set_open_time(self, time):
        self.open_time = time
        self.save()
        
    def set_close_time(self, time):
        self.close_time = time
        self.save()
        
    def set_default_open_time(self, time):
        OpeningHours.DEFAULT_OPEN_TIME_RECURRING = time
        self.save()
    
    def set_default_close_time(self, time):
        OpeningHours.DEFAULT_CLOSE_TIME_RECURRING = time
        self.save()
        
    def get_weekday_str(self):
        return self.weekdays(self.day).name

class OpeningHoursSpecific(models.Model):
    # Model for specific dates, will override recurring opening hours
    # Could have used OpeningHours as parent class, but would require some (maybe unnecessary) abstraction
    DEFAULT_OPEN_TIME = "08:00"
    DEFAULT_CLOSE_TIME = "22:00"
    date = models.DateField(null=False,blank=False,unique=True)
    open_time = models.TimeField(default=DEFAULT_OPEN_TIME)
    close_time = models.TimeField(default=DEFAULT_CLOSE_TIME)
    
    def __str__(self):
        return self.date + ":\t " + (
            self.open_time.strftime("%H:%M") + " to " +
            self.close_time.strftime("%H:%M"))
    def set_default_open_time(self, time):
        OpeningHoursSpecific.DEFAULT_OPEN_TIME = time.strftime("%H:%M")
        
    def set_default_close_time(self, time):
        OpeningHoursSpecific.DEFAULT_CLOSE_TIME = time.strftime("%H:%M")
    
    def set_open_time(self, time):
        self.open_time = time
        self.save()
        
    def set_close_time(self, time):
        self.close_time = time
        self.save()
        
    def get_weekday_str(self):
        return self.date.strftime("%A")
    
    def get_weekday_int(self):
        # 0 = Monday, 6 = Sunday
        return self.date.weekday()


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0
        IN_PROGRESS = 1
        COMPLETED = 2
        CANCELLED = 3
    
    
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    order = models.TextField()
    items = models.ManyToManyField(MenuItem)
    status = models.IntegerField()
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.name
    
    def set_pending(self):
        self.status = "Pending"
        self.save()
    
    def set_in_progress(self):
        self.status = "In Progress"
        self.save()
        
    def set_completed(self):
        self.status = "Completed"
        self.save()
        
    def set_cancelled(self):
        self.status = "Cancelled"
        self.save()


# Create your models here.
class Statistics(models.Model):
    datetime_from = models.DateTimeField()
    datetime_to = models.DateTimeField()
    
    orders = models.ManyToManyField(Order)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.date)