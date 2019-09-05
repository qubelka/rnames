from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone
from django_userforeignkey.models.fields import UserForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords

class CustomQuerySet(QuerySet):
    def delete(self):
        self.update(is_active=False)

class ActiveManager(models.Manager):
    def is_active(self):
        return self.model.objects.filter(is_active=True)

    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

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
# https://django-simple-history.readthedocs.io/en/2.6.0/index.html
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True),
        inherit=True)
# https://stackoverflow.com/questions/5190313/django-booleanfield-how-to-set-the-default-value-to-true
    is_active = models.BooleanField(default=True, help_text='Is the record active')
    objects = ActiveManager()

# https://stackoverflow.com/questions/4825815/prevent-delete-in-django-model
    def delete(self):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True


class ChoiceValue(BaseModel):
    """
    Model representing a ChoiceValue in MammalBase
    """

    choice_set = models.CharField(max_length=25, help_text="Enter the Choice Set of the ChoiceValue")
    caption = models.CharField(max_length=25, help_text="Enter the Caption of the ChoiceValue")
#    link = models.URLField(max_length=200, help_text="Enter a valid URL for the Source Reference", blank=True, null=True,)

    class Meta:
        ordering = ['choice_set','caption']
        unique_together = ('choice_set','caption',)

    def get_absolute_url(self):
        """
        Returns the url to access a particular ChoiceValue instance.
        """
        return reverse('choice-value-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s - %s ' % (self.choice_set, self.caption)


class EntityClass(BaseModel):
    """
    Model representing a Entity Class in MammalBase
    """

    name = models.CharField(max_length=25, help_text="Enter the Name of the Entity Class")
#    link = models.URLField(max_length=200, help_text="Enter a valid URL for the Source Reference", blank=True, null=True,)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular Entity Class instance.
        """
        return reverse('entity-class-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s' % (self.name)


class RelationClass(BaseModel):
    """
    Model representing a RelationClass in MammalBase
    """

    name = models.CharField(max_length=25, help_text="Enter the Name of the RelationClass")

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular RelationClass instance.
        """
        return reverse('relation-class-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s' % (self.name)


class FoodItem(BaseModel):
    """
    Model representing a FoodItem in MammalBase
    """
    name = models.CharField(max_length=250, unique=True, help_text="Enter the Name of the FoodItem")
    part = models.ForeignKey(
        'ChoiceValue',
        on_delete = models.SET_NULL,
        null = True,
        limit_choices_to={'choice_set': 'FoodItemPart'},
        )


    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular FoodItem instance.
        """
        return reverse('food-item-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s' % (self.name)


class MasterEntity(BaseModel):
    """
    Model representing a MasterEntity in MammalBase
    """
    reference = models.ForeignKey(
        'MasterReference',
        on_delete = models.CASCADE,
        )
    entity = models.ForeignKey(
        'EntityClass',
        on_delete = models.CASCADE,
        )
    name = models.CharField(max_length=250, help_text="Enter the Name of the Master Entity")

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular Master Entity instance.
        """
        return reverse('master-entity-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s' % (self.name)


class MasterReference(BaseModel):
    """
    Model representing a Master Reference in MammalBase
    """

    type = models.CharField(max_length=25, help_text="Enter the Type of the Master Reference", blank=True, null=True,)
    doi = models.URLField(max_length=200, help_text="Enter a valid DOI URL for the Master Reference", blank=True, null=True,)
    first_author = models.CharField(max_length=50, help_text="Enter the name of the first author of the Maste Reference", blank=True, null=True,)
    year = models.IntegerField(validators=[MinValueValidator(1800), MaxValueValidator(2100)], blank=True, null=True,)
    title = models.CharField(max_length=250, help_text="Enter the Title of the Master Reference", blank=True, null=True,)
    container_title = models.CharField(max_length=100, help_text="Enter the Container Title of the Master Reference", blank=True, null=True,)
    volume = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4000)], blank=True, null=True,)
    issue = models.CharField(max_length=5, help_text="Enter the Issue of the Master Reference", blank=True, null=True,)
    page = models.CharField(max_length=10, help_text="Enter the Page(s) of the Master Reference", blank=True, null=True,)
    citation = models.CharField(max_length=400, help_text="Enter the Citation of the Master Reference")
#    link = models.URLField(max_length=200, help_text="Enter a valid URL for the Source Reference", blank=True, null=True,)

    class Meta:
        ordering = ['citation']

    def get_absolute_url(self):
        """
        Returns the url to access a particular reference instance.
        """
        return reverse('master-reference-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s' % (self.citation)


class SourceEntity(BaseModel):
    """
    Model representing a SourceEntity in MammalBase
    """
    reference = models.ForeignKey(
        'SourceReference',
        on_delete = models.CASCADE,
        )
    entity = models.ForeignKey(
        'EntityClass',
        on_delete = models.CASCADE,
        )
    name = models.CharField(max_length=250, help_text="Enter the Name of the Source Entity")

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular Source Entity instance.
        """
        return reverse('source-entity-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s' % (self.name)


class EntityRelation(BaseModel):
    source_entity = models.ForeignKey(SourceEntity, on_delete=models.CASCADE)
    master_entity = models.ForeignKey(MasterEntity, on_delete=models.CASCADE)
    relation = models.ForeignKey(
        'RelationClass',
        on_delete = models.CASCADE,
        )

    class Meta:
      unique_together = ('source_entity', 'master_entity',)

    def get_absolute_url(self):
        """
        Returns the url to access a particular EntityRelation instance.
        """
        return reverse('entity-relation-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1}) {2}'.format(self.source_entity.name,self.master_entity.name,self.master_entity.reference)


class SourceReference(BaseModel):
    """
    Model representing a SourceReference in MammalBase
    """
    citation = models.CharField(max_length=250, help_text="Enter the Citation of the Source Reference")
    master_reference = models.ForeignKey(
        'MasterReference',
        on_delete = models.SET_NULL,
        blank=True,
        null=True,
        )
    STATUS = (
        (1, 'Created - Not verified'),
        (2, 'Verified - Accepted'),
        (3, 'Verified - Rejected'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, help_text='Status to Master Reference')

    class Meta:
        ordering = ['citation']

    def get_absolute_url(self):
        """
        Returns the url to access a particular reference instance.
        """
        return reverse('source-reference-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s' % (self.citation)


class DietSet(BaseModel):
    """
    Model representing a DietSet in MammalBase
    """

    reference = models.ForeignKey(
        'SourceReference',
        on_delete = models.CASCADE,
        )
    taxon = models.ForeignKey(
		SourceEntity,
		on_delete=models.CASCADE,
        limit_choices_to=Q(entity__name='Species') | Q(entity__name='Species'),
		related_name='taxon_%(class)s',
		)
    location = models.ForeignKey(
		SourceEntity,
		on_delete=models.CASCADE,
        limit_choices_to=Q(entity__name='Location') | Q(entity__name='Location'),
		related_name='location_%(class)s',
		)


    class Meta:
#        ordering = ['taxon___name']
        unique_together = ('reference','taxon','location')

    def get_absolute_url(self):
        """
        Returns the url to access a particular DietSet instance.
        """
        return reverse('diet-set-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s - %s ' % (self.taxon, self.location)


class DietSetItem(BaseModel):
    """
    Model representing a DietSetItem in MammalBase
    """

    diet_set = models.ForeignKey(
        'DietSet',
        on_delete = models.CASCADE,
        )
    food_item = models.ForeignKey(
        'FoodItem',
        on_delete = models.CASCADE,
        )

    class Meta:
        unique_together = ('diet_set', 'food_item')

    def get_absolute_url(self):
        """
        Returns the url to access a particular DietSetItem instance.
        """
        return reverse('diet-set-item-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s - %s ' % (self.diet_set, self.food_item)
