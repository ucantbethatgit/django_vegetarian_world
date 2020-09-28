from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Family(models.Model):
    """Model representing a vegetable family."""
    name = models.CharField(max_length=200, help_text='Enter a vegetable family (e.g. Root Vegetable)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Vegetable(models.Model):
    """Model representing a vegetable (but not a specific species of a vegetable)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because vegetable can only have one farmer, but farmers can have multiple vegetables
    # Farmer as a string rather than object because it hasn't been declared yet in the file
    farmer = models.ForeignKey('Farmer', on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the vegetable')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # ManyToManyField used because family can contain many vegetables. Vegetables can cover many families.
    # Family class has already been defined so we can specify the object above.
    family = models.ManyToManyField(Family, help_text='Select a family for this vegetable')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this vegetable."""
        return reverse('vegetable-detail', args=[str(self.id)])

    def display_family(self):
        """Create a string for the Family. This is required to display family in Admin."""
        return ', '.join(family.name for family in self.family.all()[:3])
    
    display_family.short_description = 'Family'

import uuid # Required for unique vegetable instances

class VegetableInstance(models.Model):
    """Model representing a specific form of a vegetable (i.e. that can be borrowed from the world)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular vegetable across whole world')
    vegetable = models.ForeignKey('Vegetable', on_delete=models.SET_NULL, null=True) 
    harvest = models.CharField(max_length=200)
    exp_date = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Vegetable availability',
    )

    class Meta:
        ordering = ['exp_date']
        permissions = (("can_mark_returned", "Set vegetable as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.vegetable.title})'

    @property
    def is_overdue(self):
        if self.exp_date and date.today() > self.exp_date:
            return True
        return False

class Farmer(models.Model):
    """Model representing a farmer."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    family = models.ManyToManyField(Family, help_text='Select a family for this vegetable')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular farmer instance."""
        return reverse('farmer-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'