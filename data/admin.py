from django.contrib import admin

from .models import Company, MasterStage, Founder, Investor, CompanyStageReport, ProductStage

class FounderInline(admin.StackedInline):
    model = Founder
    extra = 1

class CompanyStageReportInline(admin.TabularInline):
    model = CompanyStageReport
    extra = 1
    exclude = ['title', 'description', 'stage']

class CompanyAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,       {'fields': ['name', 'website', 'email_address', 'investor', 'stage']}),
    # ]
    inlines = [FounderInline, CompanyStageReportInline]

class CompanyStageReportAdmin(admin.ModelAdmin):
    fields = (
        'company', 
        'has_customers', 
        'funding', 
        'revenue', 
        'product_stage', 
        'fulltime_employees',
        'investor', 
        'date_updated',
    )
    readonly_fields = ('stage', )
    exclude = ('title', 'description')
    ordering = ('-date_updated',)

    list_display = ('__str__', 'date_updated', 'stage')
    list_display_links = ('__str__', 'stage', )
    list_filter = ('date_updated', 'stage', )
 


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyStageReport, CompanyStageReportAdmin)
admin.site.register(MasterStage)
admin.site.register(Founder)
admin.site.register(Investor)
admin.site.register(ProductStage)

