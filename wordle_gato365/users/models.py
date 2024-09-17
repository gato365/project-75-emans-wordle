from django.db import models
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('faculty_staff', 'Faculty/Staff'),
    )
    GRADUATING_CLASS_CHOICES = (
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('not_applicable', 'Not Applicable'),
    )
    COLLEGE_CHOICES = (
        ('orfalea', 'Orfalea College of Business'),
        ('bailey', 'Bailey College of Science and Mathematics'),
        ('agriculture', 'College of Agriculture, Food and Environmental Sciences'),
        ('architecture', 'College of Architecture and Environmental'),
        ('liberal_arts', 'College of Liberal Arts'),
        ('engineering', 'College of Engineering'),
        ('not_applicable', 'Not Applicable'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    graduating_class = models.CharField(max_length=20, choices=GRADUATING_CLASS_CHOICES, default='not_applicable')
    college = models.CharField(max_length=100, choices=COLLEGE_CHOICES)
    major = models.CharField(max_length=100, blank=True, null=True)

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Pass along any arguments to the parent class's save.
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()