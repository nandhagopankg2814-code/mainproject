from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to="categories")

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to="products")
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)#one time
    updated=models.DateTimeField(auto_now=True)#Each time we update the product record
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")

    def __str__(self):
        return self.name