from mongoengine import (
    Document, StringField, ReferenceField, DateTimeField, BooleanField, IntField,
)
from datetime import datetime
from mmogo.contrib.products.models import Product
from mmogo.users.models import User
from djongo import models

class Rating(models.Model):
    _id = models.ObjectIdField()
    old_id = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    object_id = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # meta = {'collection': 'ratings'}

    @property
    def document_id(self):
        if self.old_id:
            return str(self.old_id)
        else:
            return str(self._id)

    @property
    def id(self) -> str:
        # if self.old_id:
        #     return str(self.old_id)
        # else:
        return str(self._id)
    
    def __str__(self):
        return str(self.user)
    
    class Meta:
        db_table = 'ratings'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
