from django.contrib import admin

from .models import Company, Stage, Founder, Investor

class FounderInline(admin.StackedInline):
    model = Founder
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,       {'fields': ['name', 'website', 'email_address', 'investor', 'stage']}),
    # ]
    inlines = [FounderInline]

admin.site.register(Company, CompanyAdmin)
admin.site.register(Stage)
admin.site.register(Founder)
admin.site.register(Investor)

