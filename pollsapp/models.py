from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        recently = now - datetime.timedelta(days=14)
        return recently <= self.pub_date < now


    #Methods are not sortable, so sort this column in admin
    #view by pub_date:
    was_published_recently.admin_order_field = 'pub_date'
    #Instead of displaying True/False, display an icon:
    was_published_recently.boolean = True
    #Change column display from method name with underscores
    #replaced by spaces to this description:
    was_published_recently.short_description = 'Published recently?'
    
    

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text
