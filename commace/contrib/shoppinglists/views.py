import json

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import ShoppingList, ShoppingListItem, Reserved
from .serializers import (
    ShoppingListContributorSerializer, ShoppingListItemSerializer, ShoppingListSerializer,
    ReservedSerializer)

from mmogo.contrib.activities.models import Activity

class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = generics.get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

class ShoppingListsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShoppingListSerializer
    queryset = ShoppingList.objects.filter(published=True)
    

class ShoppingListView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ShoppingListSerializer
    queryset = ShoppingList.objects.all()
    lookup_field = 'id'

class FeaturedShoppingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShoppingListItemSerializer
    queryset = ShoppingList.objects.filter(featured=True)

class ShoppingListItemsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShoppingListItemSerializer
    queryset = ShoppingListItem.objects.select_related('product', 'user', 'assigned', 'shoppinglist').all()
    lookup_field = 'shoppinglist'

class ShoppingListItemView(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self, request, shoppinglist, product):
        data = request.data
        item = ShoppingListItem.objects.select_related('product', 'user', 'assigned', 'shoppinglist').get(id=product, shoppinglist__id=shoppinglist)
        if data.get('assignee'):
            user = User.objects.get(id=data.get('assignee'))
        elif item.assigned:
            user = item.assigned
        else:
            user = None
        item.quantity = data.get('quantity', item.quantity)
        item.assigned = request.user
        item.priority = data.get('priority', item.priority)
        item.status = data.get('status', item.status)
        item.save()

        Activity.objects.create(
            user = request.user,
            action = "update product quantity",
            value = f"Update product quantity",
            object_id = shoppinglist,
            content_type = ContentType.objects.get_for_model(ShoppingList),
            extra_context = { "product": product, "list_item": item.id, "type": "shoppinglist" },
        )

        return Response(ShoppingListItemSerializer(item).data, status=status.HTTP_200_OK)

    def delete(self, request, shoppinglist, product):
        item = ShoppingListItem.objects.select_related('product', 'user', 'assigned', 'shoppinglist').prefetch_related('product__images').get(id=product, shoppinglist__id=shoppinglist)
        item.delete()

        Activity.objects.create(
            user = request.user,
            action = "deleted registry product",
            value = f"Deleted registry product",
            object_id = shoppinglist,
            content_type = ContentType.objects.get_for_model(ShoppingList),
            extra_context = { "shoppinglist": shoppinglist, "list_item": product, "type": "shoppinglist" },
        )

class ShoppingListContributorsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShoppingListContributorSerializer
    queryset = ShoppingListItem.objects.all()

class ShoppingListContributorView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShoppingListContributorSerializer
    queryset = ShoppingListItem.objects.all()
    lookup_field = 'token'

class UserShoppinglistsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShoppingListSerializer
    queryset = ShoppingList.objects.all()
    lookup_field = 'user'

    def get_queryset(self):
        queryset = ShoppingList.objects.filter(user=self.request.user, published=True)
        if len(queryset) > 0:
            return queryset
        else:
            shoppinglist = ShoppingList.objects.create(
                title=f"{self.request.user.first_name}'s Registry",
                slug=f"{self.request.user.first_name.lower()}-registry",
                published=True
            )
            shoppinglist.user.add(self.request.user)

            queryset = ShoppingList.objects.prefetch_related('user').filter(user=self.request.user, published=True)
            return queryset

class ProductReservedAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ReservedSerializer
    queryset = Reserved.objects.all()
    lookup_field = 'user'

    # def post(self, request):
    #     try:
    #         serializer = ReservedSerializer(data=request.data)
    #         if serializer.is_valid():
    #             print(serializer.data)
    #         else:
    #             print(serializer.errors)
    #     except Exception as error:
    #         print(error)
