from django.db import models

# Create your models here.
class Project(models.Model):
    title= models.CharField(max_length=200)
    description= models.TextField()
    technology=models.CharField(max_length=200)
    created_at= models.DateTimeField(auto_now_add=True)
class Anemia(models.Model):
    nombreUsuario=models.CharField(max_length=200)
    Hemogobina= models.CharField(max_length=100)
    MCH=models.CharField(max_length=100)
    MCHC=models.CharField(max_length=100)
    MCV=models.CharField(max_length=100)
    Resultado=models.CharField(max_length=100)
    def __str__(self):
        return self.nombreUsuario