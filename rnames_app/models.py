from django.conf import settings
from django.db import models
from django.utils import timezone
from django_userforeignkey.models.fields import UserForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator

# https://medium.com/@KevinPavlish/add-common-fields-to-all-your-django-models-bce033ac2cdc
class BaseModel(models.Model):
    """
    A base model including basic fields for each Model
    see. https://pypi.org/project/django-userforeignkey/
    """
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, verbose_name="The user that is automatically assigned", related_name='createdby_%(class)s')
    modified_by = UserForeignKey(auto_user=True, verbose_name="The user that is automatically assigned", related_name='modifiedby_%(class)s')

    DELETED = (
        (1, 'Deleted'),
        (0, 'Active'),
    )

    is_deleted = models.PositiveSmallIntegerField(choices=DELETED, default=0, blank=True, help_text='Is the record deleted')

    class Meta:
        abstract = True

class Name(BaseModel):
    """
    Model representing a Name in RNames (e.g. Katian, Viru, etc.)
    """
    name = models.CharField(max_length=200, unique=True, help_text="Enter a Name (e.g. Katian, Viru, etc.)")


    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular name instance.
        """
        return reverse('name-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s (%s)' % (self.id,self.name)


class Reference(BaseModel):
    """
    Model representing a Reference in RNames
    """
    first_author = models.CharField(max_length=50, help_text="Enter the name of the first author of the reference", blank=True, null=True,)
    year = models.IntegerField(validators=[MinValueValidator(1800), MaxValueValidator(2100)], blank=True, null=True,)
    title = models.CharField(max_length=200, help_text="Enter the title of the reference")
    link = models.URLField(max_length=200, help_text="Enter a valid URL for the reference", blank=True, null=True,)

    class Meta:
        ordering = ["title"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular reference instance.
        """
        return reverse('reference-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s (%s, %s: %s)' % (self.id, self.first_author, self.year, self.title)

class Location(BaseModel):
    """
    Model representing a Location in RNames (e.g. Sweden, Baltoscandia, New Mexico, China, North Atlantic, etc.)
    """
    name = models.CharField(max_length=200, unique=True, help_text="Enter a Location (e.g. Sweden, Baltoscandia, New Mexico, China, North Atlantic, etc.)")


    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular name instance.
        """
        return reverse('location-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s (%s)' % (self.id,self.name)


class QualifierName(BaseModel):
    """
    Model representing a Qualifier Name in RNames (e.g. Trilobite Sub Zone, Chemo zone, Formation, my, Regional stage, etc.)
    """
    name = models.CharField(max_length=200, unique=True, help_text="Enter a Qualifier Name (e.g. Trilobite Sub Zone, Chemo zone, Formation, my, Regional stage etc.)")


    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular qualifier name instance.
        """
        return reverse('qualifier-name-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s (%s)' % (self.id,self.name)


class StratigraphicQualifier(BaseModel):
    """
    Model representing a Stratigraphic Qualifier Name in RNames (e.g. Lithostratigraphy, Chemostratigraphy, Sequence stratigraphy, Asolute age, Chronostratigraphy, Biostratigraphy, etc.)
    """
    name = models.CharField(max_length=200, unique=True, help_text="Enter a a Stratigraphic Qualifier Name (e.g. Lithostratigraphy, Chemostratigraphy, Sequence stratigraphy, Asolute age, Chronostratigraphy, Biostratigraphy, etc.)")


    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular stratigraphic qualifier instance.
        """
        return reverse('stratigraphic-qualifier-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s (%s)' % (self.id,self.name)
