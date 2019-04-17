from django.contrib import admin

# Register your models here.
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from consult.models import Theme, Specialist, TimeSlot, Enroll, Payment, Method

admin.site.register(Theme)
admin.site.register(Specialist)
admin.site.register(TimeSlot)
admin.site.register(Enroll)
admin.site.register(Payment)
admin.site.register(Method)

class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (('Advanced options'), {
            'classes': ('collapse', ),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
