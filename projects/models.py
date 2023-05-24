from django.db import models

# Create your models here.
class Project(models.Model):
    title= models.CharField(max_length=200)
    description= models.TextField()
    technology=models.CharField(max_length=200)
    created_at= models.DateTimeField(auto_now_add=True)
class Anemia(models.Model):
    nombreUsuario=models.CharField(max_length=200)
    genero = models.IntegerField(default=0)
    Hemogobina= models.CharField(max_length=100)
    MCH=models.CharField(max_length=100)
    MCHC=models.CharField(max_length=100)
    MCV=models.CharField(max_length=100)
    Resultado=models.CharField(max_length=100)
    def __str__(self):
        return self.nombreUsuario
class Diabetes(models.Model):
    nombreUsuario=models.CharField(max_length=200)
    genero = models.IntegerField(default=0)
    hipertencion=models.CharField(max_length=100)
    cardiopatia=models.CharField(max_length=100)
    fumador=models.CharField(max_length=100)
    MCI=models.CharField(max_length=100)
    nivelesHemoglobina=models.CharField(max_length=100)
    nivelGlucosa=models.CharField(max_length=100)
    edad=models.IntegerField(default=0)
    resultado=models.CharField(max_length=100)
    def __str__(self):
        return self.nombreUsuario
    
class  CancerPulmonar(models.Model):
    nombreUsuario=models.CharField(max_length=200,default='null' )
    edad=models.IntegerField()
    Genero=models.IntegerField()
    ConsumoAlcohol=models.IntegerField()
    AlergiaPolvo=models.IntegerField()
    RegistroGenetico=models.IntegerField()
    EnfermedadPulmonar=models.IntegerField()
    DietaEquilibrada=models.IntegerField()
    Obesidad=models.IntegerField()
    Tabaquismo=models.IntegerField()
    FumadorPasivo=models.IntegerField()
    DolorPecho=models.IntegerField()
    TosConSangre=models.IntegerField()
    fatiga=models.IntegerField()
    PerdidaPeso=models.IntegerField()
    DificultadRespirar=models.IntegerField()
    Sibilancia=models.IntegerField()
    DificultadTragar=models.IntegerField()
    TosSeca=models.IntegerField()
    resultados=models.CharField(max_length=100)