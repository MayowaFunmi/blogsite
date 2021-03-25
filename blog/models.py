from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone


class CustomUser(AbstractUser):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True)
    gender = models.CharField(choices=GENDER, max_length=10)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)
    interest = models.CharField(max_length=300, help_text='Indicate what contents will you like to write/read about on this blog.')
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words')


User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager
    #tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    def __str__(self):
        return self.title
