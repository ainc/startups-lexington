from django.db import models
from django.utils import timezone

# change true/false to yes/no for forms
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class Company(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateField('date created', auto_now_add=True)
    # stage = models.ForeignKey('Stage', on_delete=models.CASCADE, blank=True, null=True)
    website = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name



class Stage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    funding = models.IntegerField('Funding', default=0, blank=True, null=True)
    product_stage = models.ForeignKey('ProductStage', on_delete=models.CASCADE, blank=True, null=True)
    has_customers = models.BooleanField(choices=BOOL_CHOICES, null=True)
    revenue = models.IntegerField('Revenue', default=0, blank=True, null=True)
    fulltime_employees = models.IntegerField('Fulltime Employees', default=0, blank=True, null=True)

    def __str__(self):
        if len(self.title.split()) > 1:
            return self.title.split()[1]
        return self.title

class CompanyReport(Stage):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE, blank=True, null=True)
    date_updated = models.DateField('Date updated')

    def save(self, *args, **kwargs):
        # on save, update timestamps
        self.date_updated = datetime.date.today()
        return super(CompanyReport, self).save(*args, **kwargs)
        

class Founder(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    linked_in = models.URLField(blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

class Investor(models.Model):
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    website = models.URLField()

    def __str__(self):
        return self.name

class ProductStage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class CompanyComment(models.Model):
    content = models.TextField()
    date_added = models.DateTimeField('date', auto_now_add=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)