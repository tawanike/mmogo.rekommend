from django.contrib.auth.models import User

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from mmogo.contrib.notifications.models import Notification
from mmogo.profiles.models import Profile

from zoozoo.relatives.graphql.schema import GuestSchema

class UserType(DjangoObjectType):
  class Meta:
    model = User


class ProfileType(DjangoObjectType):
  user = graphene.Field(UserType)
  class Meta:
    model = Profile

class NotificationType(DjangoObjectType):
  sender = graphene.Field(UserType)
  status = graphene.String(source='status_display')

  class Meta:
    model = Notification
    interfaces = (relay.Node,) 
    fields = ('id', 'title', 'sender', 'user', 'status', 'created_at', 'extra_context', 'image')

class UpdateNotification(graphene.Mutation):
  class Arguments:
    status = graphene.Int(required=True)
    id = graphene.Int(required=True)

  notification = graphene.Field(NotificationType)

  @classmethod
  def mutate(cls, root, info, id, status):
    notification = Notification.objects.get(id=id)
    notification.status = status
    notification.save()

    return UpdateNotification(notification=notification)
class Query(GuestSchema, graphene.ObjectType):
    all_notifications = graphene.List(NotificationType)
    notifications = graphene.List(NotificationType, user=graphene.Int(required=True))

    def resolve_all_notifications(root, info, **kwargs):
      # Querying a list
      return Notification.objects.all().order_by('-created_at')

    def resolve_notifications(root, info, **kwargs):
      # Querying a list
      return Notification.objects.filter(user=kwargs.get('user')).order_by('created_at')

class Mutation(graphene.ObjectType):
  update_notification = UpdateNotification.Field()

schema = graphene.Schema(
  query=Query,
  mutation=Mutation
)