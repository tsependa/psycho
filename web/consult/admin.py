from django.contrib import admin

# Register your models here.
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from consult.models import Theme, Specialist, TimeSlot, Enroll, Payment, Method, Faq, SupportQuestion

admin.site.register(Theme)
admin.site.register(Specialist)

admin.site.register(Enroll)
admin.site.register(Payment)
admin.site.register(Method)
admin.site.register(Faq)



class EnrollInline(admin.StackedInline):
    model = Enroll


class TimeslotAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialist', 'start_time', 'enroll', 'has_payment', 'videoconf_url')
    list_filter = ('specialist', 'start_time')
    list_select_related = ('enroll',)
    inlines = (EnrollInline,)

    def has_payment(self, obj):
        return bool(obj.enroll.payment)
    has_payment.boolean = True


admin.site.register(TimeSlot, TimeslotAdmin)


class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


class SupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'question', 'created_at')

admin.site.register(SupportQuestion, SupportAdmin)

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
