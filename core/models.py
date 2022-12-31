from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
from django.db import models

# from ckeditor.fields import RichTextField
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('User must have an username')
        

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), password=password, username=username)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    address = models.TextField(max_length=300, null=True)
    status = models.IntegerField(null=True)
    verification_code = models.IntegerField(null=True)
    create_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='last login', auto_now=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(upload_to='image')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    object = MyAccountManager()

    def delete(self, *args, **kwargs):
        # first, delete the file
        self.image.delete(save=False)

        # now, delete the object
        super(User, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            this = User.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except:
            pass
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class blog_model(models.Model):
    topic = models.CharField(max_length=200,null=True)
    title = models.CharField(max_length=200)
    short_description = models.TextField(default='',max_length=50)
    description = models.TextField(default='',max_length=5000)
    thumbnail = models.FileField(upload_to='images', null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-update_at', '-create_at']
    def __str__(self):
        return self.title
# class Room(models.Model):
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=200)
#     video = EmbedVideoField()
#     description = models.TextField(null=True, blank=True)
#     participants = models.ManyToManyField(
#         User, related_name='participants', blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.name


# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[0:50]


class ourTeam(models.Model):
    name = models.CharField(null=False, max_length=200)
    rank = models.CharField(null=False, max_length=500)
    image = models.ImageField(upload_to='image', null=True)
    facebook = models.CharField(null=True, max_length=500)
    twitter = models.CharField(null=True, max_length=500)
    google = models.CharField(null=True, max_length=500)
    whatapp = models.CharField(null=True, max_length=500)

   