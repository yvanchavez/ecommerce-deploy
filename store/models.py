from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)

from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario', max_length=30, unique=True)
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nombre', max_length=100, blank=True)
    is_active = models.BooleanField('Esta activo?', blank=True, default=True)
    is_staff = models.BooleanField('Es del Equipo?', blank=True, default=True)
    date_joined = models.DateTimeField('Fecha de Registro', auto_now_add=True)
    foto = models.ImageField(upload_to='perfil' , blank=True , null=True)
    #Crear el superusuario
    objects = UserManager()
    #Una cadena que describe el nombre del campo en el modelo de usuario
    # que se utiliza como identificador único. Por lo general, será un nombre de
    # usuario de algún tipo, pero también puede
    # ser una dirección de correo electrónico o cualquier otro identificador único
    USERNAME_FIELD = 'username'
    #Una lista de los nombres de campo que se solicitarán al crear un usuario
    # mediante el createsuperuser
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.name or self.username
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'usuarios'

class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Usuario",
        related_name='resets', on_delete=models.CASCADE
    )
    key = models.CharField('Clave', max_length=100, unique=True)
    created_at = models.DateTimeField("Creado en", auto_now_add=True)
    confirmado = models.BooleanField("Confirmado?", default=False, blank=True)

    def __str__(self):
        return '{0} en {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nueva Contraseña'
        verbose_name_plural = 'Nueva Contraseñas'
        ordering = ['-created_at']


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField("nombre",max_length=200)
    price = models.DecimalField("Precio",max_digits=7, decimal_places=2)
    categories = models.ManyToManyField(Category,verbose_name=('Categorias'))
    digital = models.BooleanField(default=False, null=True, blank=False)
    image1 = models.ImageField("Imagen 1",upload_to="productos", null=True, blank=True)
    image2 = models.ImageField("Imagen 2",upload_to="productos", null=True, blank=True)
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total




class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=200, null=False)
    provincia = models.CharField(max_length=200, null=False)
    distrito = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.direccion




