from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from rnames_app.models import Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName, Relation
from mb import models

# admin.site.register([Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName, Relation,])

#@admin.register(Name)
#class NameAdmin(admin.ModelAdmin):
#    list_display = ['name', ]
#    search_fields = ['name', ]
#    history_list_display = ['name', ]

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['first_author', 'year', 'title', ]
    list_display_links = ['first_author', ]
    search_fields = ['first_author', 'title', ]

class RelationAdmin(admin.ModelAdmin):
    raw_id_fields = ('name_one', 'name_two',)
#    search_fields = ['structuredname__name']
#    search_fields = ['foreign_key__related_fieldname']

class RelationHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ['belongs_to', ]
    raw_id_fields = ('name_one', 'name_two',)
    search_fields = ['name_one__name__name', 'name_two__name__name', ]

class StructuredNameHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ['qualifier', 'name', 'location', ]
    search_fields = ['name__name', ]

admin.site.register(Name, SimpleHistoryAdmin)
#admin.site.register(Reference, SimpleHistoryAdmin)
admin.site.register(Location, SimpleHistoryAdmin)
admin.site.register(QualifierName, SimpleHistoryAdmin)
admin.site.register(StratigraphicQualifier, SimpleHistoryAdmin)
admin.site.register(Qualifier, SimpleHistoryAdmin)
#admin.site.register(StructuredName, SimpleHistoryAdmin)
admin.site.register(Relation, RelationHistoryAdmin)
admin.site.register(StructuredName, StructuredNameHistoryAdmin)
admin.site.register(models.ChoiceValue, SimpleHistoryAdmin)
admin.site.register(models.DietSet, SimpleHistoryAdmin)
admin.site.register(models.DietSetItem, SimpleHistoryAdmin)
admin.site.register(models.EntityClass, SimpleHistoryAdmin)
admin.site.register(models.EntityRelation, SimpleHistoryAdmin)
admin.site.register(models.FoodItem, SimpleHistoryAdmin)
admin.site.register(models.MasterEntity, SimpleHistoryAdmin)
admin.site.register(models.MasterReference, SimpleHistoryAdmin)
admin.site.register(models.RelationClass, SimpleHistoryAdmin)
admin.site.register(models.SourceEntity, SimpleHistoryAdmin)
admin.site.register(models.SourceReference, SimpleHistoryAdmin)
