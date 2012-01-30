from django.db import models

# Create your models here.

class Location(models.Model):
    """model for location"""
    name = models.CharField(max_length=129)
    detail = models.TextField(blank=True)

    is_root = models.BooleanField(default=False)
    parent = models.ForeignKey(Location)
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('location' )

