from django.db import models

# Create your models here.

# City where employees live 
class City(models.Model):
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name

# Employee title 
class Title(models.Model):
    title_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title_name

class Employee(models.Model):
    employee_name = models.CharField(max_length=255)
    employee_city = models.ForeignKey(
        City,
        related_name='employee_city',on_delete='cascade'
    )
    employee_title = models.ForeignKey(
        Title,
        related_name='employee_title',on_delete='cascade'
    )
    def __str__(self):
        return self.employee_name
