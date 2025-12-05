from django.db import models

class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200, blank=True)

    selected_package = models.CharField(max_length=200, blank=True)

    starting_location = models.CharField(max_length=200, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    travel_group = models.CharField(max_length=100, blank=True)

    nights = models.IntegerField(default=1)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)

    hotel_category = models.CharField(max_length=100, blank=True)
    transportation = models.CharField(max_length=100, blank=True)

    extra_requirement = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
