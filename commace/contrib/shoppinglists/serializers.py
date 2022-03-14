import uuid
import random
import string

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.template import Context, Engine
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from altur.email.models import Email
from altur.sms.utils import generate_mobile_code

from mmogo.contrib.activities.serializers import ActivitySerializer
from mmogo.contrib.activities.models import Activity
from mmogo.profiles.serializers import UserSerializer
from mmogo.contrib.locations.models import Country
from mmogo.contrib.invitations.models import Invite
from mmogo.profiles.models import Profile


from .models import ShoppingListContributor,  ShoppingListItem, ShoppingList, Reserved

from commace.products.serializers import ProductSerializer
from commace.products.models import Product


def create_token():
    new_token = uuid.uuid4()
    try:
        ShoppingListContributor.objects.get(token=new_token)
        return create_token()
    except ShoppingListContributor.DoesNotExist:
        return new_token

class ShoppingListContributorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, write_only=True)
    last_name = serializers.CharField(max_length=255, write_only=True)
    email = serializers.CharField(max_length=255, write_only=True)
    user = serializers.IntegerField(write_only=True)

    def to_representation(self, instance):
        representation = super(ShoppingListContributorSerializer, self).to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        
        if instance.invitee:
            representation['invitee'] = UserSerializer(User.objects.get(email=instance.invitee)).data
        return representation

    def create(self, validated_data):
        group = Group.objects.get(name='Users')
        password = token = create_token()
        mobile_token = generate_mobile_code()
        invitation_code = ''.join(random.choice(string.ascii_letters) for x in range(7))

        with transaction.atomic():
            user = User.objects.get(id=validated_data['user'])
            invitee = User.objects.filter(email=validated_data['email']).first()
            if not invitee:
                try:
                    invitee = User()
                    invitee.first_name = validated_data['first_name']
                    invitee.last_name = validated_data['last_name']
                    invitee.email = validated_data['email']
                    invitee.username = validated_data['email']
                    invitee.is_active = False
                    invitee.set_password(password)
                    invitee.save()
                    invitee.groups.set(group)

                    Profile.objects.create(
                        user=invitee,
                        token=token,
                        country=Country.objects.get(slug='south-africa'),
                        mobile_token=mobile_token,
                        invitation_code=invitation_code
                    )

                except Exception as error:
                    print('User', error)

            engine = Engine.get_default()
            context = Context({
                "invitee": invitee.first_name,
                "token": token,
                "user": str(f'{user.first_name} {user.last_name}')
            })

            contributor = ShoppingListContributor.objects.create(
                shoppinglist=ShoppingList.objects.get(id=validated_data['shoppinglist'].id),
                user=user,
                invitee=invitee,
                token=token,
            )

            template = engine.get_template('email/invitation.html')
            context = Context(context)
            body = template.render(context)

            Email.objects.create(
                subject="ZowZow Baby Gift Registry Invitation.",
                from_address=settings.POSTMAN,
                body=body,
                recipient=invitee,
                service='SES',
            )
            
            return contributor

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = ShoppingListContributor
        fields = '__all__'
        read_only_fields = ['invitee', 'role', 'invite_accepted']

class  ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = '__all__'

class ShoppingListItemSerializer(serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)
    product = serializers.IntegerField(write_only=True)
    shoppinglist = serializers.IntegerField(write_only=True)
    user = serializers.IntegerField(write_only=True)
    class Meta:
        model = ShoppingListItem
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        representation = super(ShoppingListItemSerializer, self).to_representation(instance)
        try:
            representation['product'] = ProductSerializer(Product.objects.get(id=instance['product'])).data
        except Exception:
            try:
                representation['product'] = ProductSerializer(instance.product).data
            except Exception:
                representation['product'] = ProductSerializer(instance.get('product')).data

        return representation

    def update(self, instance, validated_data):
        priority = validated_data['priority']
        status = validated_data['status']
        quantity = validated_data['quantity']
        product = validated_data['product']
        shoppinglist = validated_data['shoppinglist']
        user = validated_data['user']

        try:
            user = ShoppingListContributor.objects.get(user__id=user, shoppinglist__id=shoppinglist)
        except ShoppingListContributor.DoesNotExist:
            message = 'You need to be the owner or a contributor to modify this shopping list'
            return {'message': message}

        try:
            item = ShoppingListItem.objects.get(id=product, shoppinglist__id=shoppinglist)
            item.quantity = quantity
            item.priority = priority
            item.status = status
            item.save()

            Activity.objects.create(
                user = user,
                action = "update product quantity",
                value = f"Update product quantity",
                object_id = validated_data['shoppinglist'],
                content_type = ContentType.objects.get_for_model(ShoppingListItem.shoppinglist),
                extra_context = { "product": validated_data['product'], "list_item": item.id },
            )

            return item
        except Exception as error:
                return error

    def create(self, validated_data):
        try:
            user = User.objects.get(id=validated_data['user'])
            shoppinglist = ShoppingList.objects.get(id=validated_data['shoppinglist'])
            item = ShoppingListItem.objects.get(product=validated_data['product'], shoppinglist=shoppinglist)
            item.quantity += 1
            item.save()

            # Activity.objects.create(
            #     user = user,
            #     action = "add product",
            #     value = f"Add product",
            #     object_id = shoppinglist,
            #     content_type = ContentType.objects.get_for_model(ShoppingListItem.shoppinglist),
            #     extra_context = { "product": validated_data['product'], "list_item": item.id },
            # )
            return item

        except ShoppingListItem.DoesNotExist:
            user = User.objects.get(id=validated_data['user'])
            item = ShoppingListItem.objects.create(
                user = user,
                shoppinglist = ShoppingList.objects.get(id=validated_data['shoppinglist']),
                product = Product.objects.get(id=validated_data['product']),
                quantity = 1
            )

            # Activity.objects.create(
            #     user = user,
            #     action = "add product to registry",
            #     value = f"Product added to registry.",
            #     object_id = validated_data['shoppinglist'],
            #     content_type = ContentType.objects.get_for_model(ShoppingList),
            #     extra_context = { "product": validated_data['product'] }
            # )

            return item
        except Exception as error:
            return {
                'code': 500,
                'message': str(error)
            }

class  ShoppingListSerializer(serializers.ModelSerializer):
    products = ShoppingListItemSerializer(many=True, read_only=True, source="shoppinglists")

    def to_representation(self, instance):
        representation = super(ShoppingListSerializer, self).to_representation(instance)
        representation['contributors'] = [UserSerializer(contributor.user).data for contributor in instance.user.through.objects.filter(invite_accepted=True)]
        # representation['activities'] = ActivitySerializer(
        #     Activity.objects.select_related('user', 'content_type').filter(object_id=instance.id).order_by('-created_at'), many=True
        # ).data
        return representation

    def create(self, validated_data):
        user = self.context['request'].user
        get_user = get_object_or_404(User, email=user)
        validated_data['user'] = get_user

        return super().create(validated_data)

    class Meta:
        model = ShoppingList
        fields = '__all__'
        read_only_fields = ['user']

class ReservedSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super(ReservedSerializer, self).to_representation(instance)
        try:
            representation['product'] = ShoppingListItemSerializer(instance.product).data
            representation['registry'] = ListSerializer(instance.product.shoppinglist).data
        except Exception as error:
            print(error)

        return representation
    class Meta:
        model = Reserved
        fields = '__all__'
