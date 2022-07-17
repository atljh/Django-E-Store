from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_by_id(category_id):
        return Category.objects.get(id=category_id)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    @staticmethod
    def get_subcategories(category_id):
        return SubCategory.objects.filter(category=category_id)

    @staticmethod
    def get_items():
        return SubCategory.objects.all()

    def __str__(self):
        return self.name


# class Customer(models.Model):
#     username = models.CharField(max_length=30)
#     email = models.EmailField(max_length=40)
#     password = models.CharField(max_length=100)
#
#     def register(self):
#         self.save()
#
#     @staticmethod
#     def get_customer_by_email(email):
#         try:
#             return Customer.objects.get(email=email)
#         except:
#             return False
#
#     def is_exists(self):
#         if Customer.objects.filter(email=self.email):
#             return True
#         return False
#
#     def __str__(self):
#         return self.username


class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    date_created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()


    @staticmethod
    def get_with_filters(ctgry, min_price, max_price):
        if ctgry != 'all':
            return Product.objects.filter(category=ctgry, price__gte=min_price, price__lte=max_price)
        return Product.objects.filter(price__gte=min_price, price__lte=max_price)


    @staticmethod
    def get_all_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    @staticmethod
    def get_all_subcategoryid(subcategory_id):
        if subcategory_id:
            return Product.objects.filter(subcategory=subcategory_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    name = models.CharField(max_length=50, default='', blank=True)
    surname = models.CharField(max_length=50, default='', blank=True)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def order_save(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
