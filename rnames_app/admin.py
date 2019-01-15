from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName, Relation

# admin.site.register([Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName, Relation,])

class RelationHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ['belongs_to']
    raw_id_fields = ('name_one', 'name_two',)

class RelationAdmin(admin.ModelAdmin):
    raw_id_fields = ('name_one', 'name_two',)

class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['first_author', 'year', ]
    list_display_links = ['first_author', ]
    search_fields = ['first_author', ]

admin.site.register(Name, SimpleHistoryAdmin)
admin.site.register(Reference, SimpleHistoryAdmin)
admin.site.register(Location, SimpleHistoryAdmin)
admin.site.register(QualifierName, SimpleHistoryAdmin)
admin.site.register(StratigraphicQualifier, SimpleHistoryAdmin)
admin.site.register(Qualifier, SimpleHistoryAdmin)
admin.site.register(StructuredName, SimpleHistoryAdmin)
admin.site.register(Relation, RelationHistoryAdmin)
