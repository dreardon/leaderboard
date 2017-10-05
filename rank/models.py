from django.db import models
from django.conf import settings

class Sprint(models.Model):
    name = models.CharField(max_length=100)
    isActive = models.BooleanField()

    def __str__(self):
        return "{0} {1} {2}".format(self.name,'(Active: ',str(self.isActive)+')')

class Team(models.Model):
    name = models.CharField(max_length=100)
    isActive = models.BooleanField()
    profile_pic = models.ImageField(upload_to='media',null=True, blank=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.name,'(Active: ',str(self.isActive)+')')


class Criteria(models.Model):
    name  = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    isActive = models.BooleanField()

    class Meta:
        verbose_name_plural = "Criteria"

    def __str__(self):
        return "{0} {1} {2}".format(self.name,'(Active: ',str(self.isActive)+')')


class Ranking(models.Model):
    sprint = models.ForeignKey(Sprint, null=False, blank=False)
    team = models.ForeignKey(Team, null=False, blank=False)
    criteria = models.ForeignKey(Criteria, null=False, blank=False)
    points = models.DecimalField(default=0.0, max_digits=5, decimal_places=1)
    dataDate = models.DateField(null=False, blank=False)
    lastModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.sprint,self.team,self.criteria,self.points,self.dataDate)

class SystemMessage(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(null=False, blank=False)
    isActive = models.BooleanField()
    lastModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.name, self.isActive,self.lastModified)
