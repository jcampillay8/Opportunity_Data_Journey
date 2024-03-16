# from django.db import models

# class Request(models.Model):
#     DROPDOWN_CHOICES = [
#         ('option1', 'Opción 1'),
#         ('option2', 'Opción 2'),
#         # Agrega más opciones aquí
#     ]

#     text = models.CharField(max_length=200)
#     number = models.IntegerField()
#     date = models.DateField()
#     dropdown = models.CharField(max_length=200, choices=DROPDOWN_CHOICES)
#     checkbox1 = models.BooleanField()
#     checkbox2 = models.BooleanField()
#     checkbox3 = models.BooleanField()
#     radios = models.CharField(max_length=200)
#     range = models.IntegerField()
#     file = models.FileField(upload_to='uploads/')
#     textarea = models.TextField()
