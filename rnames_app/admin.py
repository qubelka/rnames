from django.contrib import admin
from .models import Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName

admin.site.register([Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName,])
