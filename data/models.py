from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added', auto_now_add=True)
    stage = models.ForeignKey('Stage', on_delete=models.CASCADE, blank=True, null=True)
    website = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE, blank=True, null=True)
    

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

class CompanyStage(models.Model):
    funding = models.IntegerField('Funding', default=0, blank=True, null=True)
    product_stage = models.ForeignKey('ProductStage', blank=True, null=True)

class Stage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    funding = models.IntegerField('Funding', default=0, blank=True, null=True)
    product_stage = models.ForeignKey('ProductStage', blank=True, null=True)
    has_customers = 

    def __str__(self):
        if len(self.title.split()) > 1:
            return self.title.split()[1]
        return self.title

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