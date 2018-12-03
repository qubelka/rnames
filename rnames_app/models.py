from django.conf import settings
from django.db import models
from django.utils import timezone


class Name(models.Model):
    """
    Model representing a Name in RNames (e.g. Katian, Viru, etc.)
    """
    name = models.CharField(max_length=200, help_text="Enter a Name (e.g. Katian, Viru, etc.)")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        return self.name
