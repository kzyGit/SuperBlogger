from rest_framework import status
from ..models import Articles
from ..serializers import ArticleSerializer
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, )
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import PermissionDenied, NotFound
from ..utils import CheckSlug, IsOwner


class ArticlesView(ViewSet):
    queryset = Articles.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ArticleSerializer

    def post(self, request):
        article = request.data
        serializer = self.serializer_class(data=article,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        data = {
            'message': 'article created successfully',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, slug=None):
        """ Get all articles """
        if (slug):
            try:
                serializer = self.serializer_class(Articles.objects
                                                   .get(slug=slug))
            except Exception:
                raise NotFound({'error': 'No article with that slug'})
        else:
            serializer = self.serializer_class(
                Articles.objects.all(), many=True)
        return Response(serializer.data)

    def get_mine(self, request):
        """ Get my articles """
        try:
            articles = Articles.objects.filter(user=request.user)
            serializer = self.serializer_class(articles.all(), many=True)
            data = serializer.data if serializer.data else {
                'message': 'Sorry you have no articles yet'}
            return Response(data)

        except Exception:
            raise PermissionDenied(
                {'message': 'Login first to view your articles'})

    def delete(self, request, slug=None):
        article = CheckSlug(slug, Articles, 'article', 'deleted')
        IsOwner(request, article)
        article.delete()
        return Response({'message': 'Article deleted successfully'},
                        status=status.HTTP_200_OK)

    def update(self, request, slug=None):
        article = CheckSlug(slug, Articles, 'article', 'updated')
        serializer = self.serializer_class(article, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'article updated successfully',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
