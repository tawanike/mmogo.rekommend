from datetime import datetime
from mongoengine import (
    Document, StringField, ReferenceField, IntField, BooleanField,
    DateTimeField, 
)

from mmogo.users.models import User
from djongo import models


class Company(models.Model):
    _id = models.ObjectIdField()
    old_id = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_company')
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    cover = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)
    is_promoted = models.BooleanField(default=False)
    is_claimed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # meta = {'collection': 'companies'}

    def __str__(self) -> str:
        return str(self.title)

    @property
    def id(self):
        # if self.old_id:
        #     return str(self.old_id)
        # else:
        return str(self._id)
    
    class Meta:
        managed = False
        db_table = 'companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companiedd'
