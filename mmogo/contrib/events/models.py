from django.db import models
from django.contrib.auth.models import User

from mmogo.contrib.medialibrary.models import MediaLibrary

'''
    TODO Calendar and Events should be in separate models such that then you create an event, it gets added
         to the calendar, when you create a checklist item with a due date, it is also added to the calendar
'''

class Event(models.Model):
    APPOINTMENT = 0
    EVENT = 1

    EVENT_TYPES = (
        (APPOINTMENT, 'Appointment'),
        (EVENT, 'Event'),
    )

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    cover = models.ImageField(upload_to='events/covers/', null=True, blank=True)
    owner = models.ForeignKey(User, related_name='userevents', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='eventrsvps', null=True, blank=True, through='RSVP')
    published = models.BooleanField(default=False)
    location = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    event_type = models.IntegerField(default=APPOINTMENT, choices=EVENT_TYPES)
    attachments = models.ManyToManyField(MediaLibrary, related_name='eventattachments', null=True, blank=True)
    reminder = models.IntegerField(default=10)
    is_all_days = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        db_table = 'events'
        ordering = ['start_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    @property
    def start_date_time(self):
        return '' # TODO Create date_time object

    @property
    def end_date_time(self):
        return '' # TODO Create date_time object

class RSVP(models.Model):
    PENDING = 0
    YES = 1
    MAYBE = 2
    NO = 3

    RSVP_CHOICES = (
        (PENDING, 'Pending'),
        (YES, 'Yes'),
        (MAYBE, 'Maybe'),
        (NO, 'No'),
    )
    user = models.ForeignKey(User, related_name='user_rsvp', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='eventrsvp', on_delete=models.CASCADE)
    status = models.IntegerField(default=PENDING, choices=RSVP_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)