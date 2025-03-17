from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class District(models.Model):
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return self.district_name

    

class Area(models.Model):
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    area_name = models.CharField(max_length=100)

    def __str__(self):
        return self.area_name

    
class Business_type(models.Model):
    business_type = models.CharField(max_length=100)
    business_image = models.ImageField(upload_to='businness_type_images/',null=False,blank=False)

    def __str__(self):
        return self.business_type


from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    business_type = models.ForeignKey(Business_type, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100, null=False, blank=False)
    business_description = models.TextField()
    business_since = models.CharField(max_length=100, null=False, blank=False)
    business_contact = models.CharField(max_length=100, null=False, blank=False)
    business_whatsapp = models.CharField(max_length=100, null=False, blank=False)
    
    # Business Images
    business_image_1 = models.ImageField(upload_to='businness_images/', null=False, blank=False)
    business_image_2 = models.ImageField(upload_to='businness_images/', null=True, blank=True)
    business_image_3 = models.ImageField(upload_to='businness_images/', null=True, blank=True)
    business_image_4 = models.ImageField(upload_to='businness_images/', null=True, blank=True)
    business_image_5 = models.ImageField(upload_to='businness_images/', null=True, blank=True)

    # Social Links
    business_instagram_link = models.URLField(null=True, blank=True)
    business_facebook_link = models.URLField(null=True, blank=True)
    business_youtube_link = models.URLField(null=True, blank=True)
    business_x_link = models.URLField(null=True, blank=True)

    # Location and Slug
    business_location = models.URLField(null=True, blank=True)
    business_slug = models.SlugField(unique=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        if not self.business_slug:  # Only generate slug if not provided
            base_slug = slugify(self.business_name)
            unique_slug = base_slug
            counter = 1

            while Business.objects.filter(business_slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.business_slug = unique_slug

        super().save(*args, **kwargs)


class Service_type(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='businness_images/',null=False,blank=False)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    service_type = models.ForeignKey(Service_type, on_delete=models.CASCADE)
    image_1 = models.ImageField(upload_to='businness_images/',null=False,blank=False)
    image_2 = models.ImageField(upload_to='businness_images/',null=True,blank=True)
    image_3 = models.ImageField(upload_to='businness_images/',null=True,blank=True)
    image_4 = models.ImageField(upload_to='businness_images/',null=True,blank=True)
    image_5 = models.ImageField(upload_to='businness_images/',null=True,blank=True)
    age = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    instagram_link = models.URLField()
    facebook_link = models.URLField()
    youtube_link = models.URLField()
    x_link = models.URLField()
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
