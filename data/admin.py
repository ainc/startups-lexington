from django.contrib import admin

from .models import Company, Stage, Founder, Investor, CompanyReport, ProductStage

class FounderInline(admin.StackedInline):
    model = Founder
    extra = 1

class CompanyReportInline(admin.StackedInline):
    model = CompanyReport
    extra = 1
    exclude = ['title', 'description']

class CompanyAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,       {'fields': ['name', 'website', 'email_address', 'investor', 'stage']}),
    # ]
    inlines = [FounderInline, CompanyReportInline]

class CompanyReportAdmin(admin.ModelAdmin):
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
    exclude = ('title', 'description')



admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyReport, CompanyReportAdmin)
admin.site.register(Stage)
admin.site.register(Founder)
admin.site.register(Investor)
admin.site.register(ProductStage)

