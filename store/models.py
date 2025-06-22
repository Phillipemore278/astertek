import uuid
import secrets
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            count = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("frontend:category_detail", args=[self.slug])
    

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            count = 1
            while Brand.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            count = 1
            while Tag.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True, related_name='products')
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    image = CloudinaryField('image', null=True, default=None, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0, help_text="Rate from 1 (worst) to 5 (best)")

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        while Product.objects.filter(slug=slug).exists():
            unique_part = f"{uuid.uuid4().hex[:4]}-{secrets.token_hex(2)}"
            slug = f"{unique_part}-{base_slug}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)


    @property
    def sale_percent(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return round(discount, 1)  # Rounded to 1 decimal
        return 0

    def __str__(self):
        return self.name
