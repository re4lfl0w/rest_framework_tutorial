from django.contrib.auth.models import User
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from rest_framework import renderers
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from snippets.permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    이 뷰셋은 'list'와 'detail' 기능을 자동으로 지원합니다.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    '''
    이 뷰셋은 'list'와 'create', 'retrieve', 'update', 'destroy' 기능을 자동으로 지원합니다
    여기에 'highlight' 기능의 코드만 추가로 작성했습니다.
    '''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)