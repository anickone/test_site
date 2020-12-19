from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from datetime import datetime
from PIL import Image
import os
import logging
import time
from .serializers import UserSerializer, ProductSerializer
from .models import Product
from .permissions import IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


def log(user, action, uuid):
    logger.info(f'INFO: Username="{user}" {action} product uuid="{uuid}"'
                f' on time {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}')


def rotate(path):
    start_time = time.time()
    path_img = os.path.join(settings.MEDIA_ROOT, path)
    im = Image.open(path_img)
    im.transpose(Image.ROTATE_180).save(path_img)
    return time.time() - start_time


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        if instance.logo:
            time_rotate = rotate(instance.logo.name)
            instance.rotate_duration = time_rotate
            instance.save()
        log(self.request.user, 'created', instance.id)

    def list(self, request, *args, **kwargs):
        query = request.query_params
        if 'modified' in query and query['modified'].lower() == 'true':
            queryset = Product.objects.filter(modified=True)
        elif 'modified' in query and query['modified'].lower() == 'false':
            queryset = Product.objects.filter(modified=False)
        else:
            queryset = self.queryset

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save(owner=self.request.user)
        if instance.logo:
            time_rotate = rotate(instance.logo.name)
            instance.rotate_duration = time_rotate
            instance.save()
        log(self.request.user, 'updated', instance.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.modified:
            raise serializers.ValidationError('Update limit has been reached.')
        instance.modified = True
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        uuid = instance.id
        instance.delete()
        log(self.request.user, 'deleted', uuid)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products-users': reverse('user-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format)
    })
