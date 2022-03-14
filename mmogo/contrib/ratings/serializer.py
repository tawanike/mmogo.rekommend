from mmogo.contrib.products.serializers import product_serializer


def rating_serializer(rating):
    return {
        'id': rating.document_id,
        'created_at': rating.created_at,
        'updated_at': rating.updated_at,
        'user': rating.user,
        'rating': rating.rating,
        'object_id': rating.object_id,
        'object_type': rating.object_type
    }
