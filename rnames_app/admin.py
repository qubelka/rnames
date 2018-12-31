from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName, Relation

# admin.site.register([Name, Reference, Location, QualifierName, StratigraphicQualifier, Qualifier, StructuredName, Relation,])

class RelationHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ["belongs_to"]

admin.site.register(Name, SimpleHistoryAdmin)
admin.site.register(Reference, SimpleHistoryAdmin)
admin.site.register(Location, SimpleHistoryAdmin)
admin.site.register(QualifierName, SimpleHistoryAdmin)
admin.site.register(StratigraphicQualifier, SimpleHistoryAdmin)
admin.site.register(Qualifier, SimpleHistoryAdmin)
admin.site.register(StructuredName, SimpleHistoryAdmin)
admin.site.register(Relation, RelationHistoryAdmin)
