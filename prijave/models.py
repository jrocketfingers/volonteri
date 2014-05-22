from datetime import datetime, timedelta
from django.db import models

# Create your models here.
class Poziv(models.Model):
    lokacija = models.CharField(max_length=200)
    opis = models.TextField()
    kolicina_pomoci = models.IntegerField()
    prijavljeno_pomoci = models.IntegerField(default = 0)

    datum_isteka = models.DateTimeField(default = datetime.now() + timedelta(hours = 2))

    def progress(self):
        return min(float(self.prijavljeno_pomoci) / float(self.kolicina_pomoci) * 100, 100)

    def __unicode__(self):
        return self.lokacija
