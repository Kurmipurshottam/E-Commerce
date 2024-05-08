from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    user_type=models.CharField(default="buyer",max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=40)
    picture = models.ImageField(default="profile/default-picture.png",upload_to="profile/")


    def __str__(self):
        return  self.first_name
      
    
class Product(models.Model):
    category = (
        ("Men","Men"),
        ("Women","Women"),
        ("Child","Child")
    )
    size = (
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL")
    )
    brand = (
        ("Levis","Levis"),
        ("Roadstar","Roadstar"),
        ("Nike","Nike")
    )
    product_category = models.CharField(max_length=40,choices=category,null=True)
    product_size = models.CharField(max_length=40,choices=size,null=True)
    product_brand = models.CharField(max_length=40,choices=brand,null=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    product_name = models.CharField(max_length=40)
    description = models.TextField()
    product_picture = models.ImageField(default="IMAGE NOT FOUND",upload_to="product/")

    def __str__(self):
        return self.product_name + " || " + self.product_brand
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.first_name + " || " + self.product.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1)  
    cart_price =  models.PositiveIntegerField()
    total_price = models.PositiveSmallIntegerField(default=0)
    # pyment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " || " + self.product.product_name 
    
class Order_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.PositiveBigIntegerField()

    def __str__(self):
        return self.user.first_name + " || " + self.address
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # product = models.ForeignKey(Product,on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.PositiveBigIntegerField()
    contact = models.CharField(max_length=15)
    total_price = models.PositiveSmallIntegerField()  
    pyment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.contact + " || " + self.address
