from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle
from rest_framework import filters

from .models import Achievement, Cat, User
from .premissions import OwnerOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .pagination import CatsPagination

from django_filters.rest_framework import DjangoFilterBackend


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (AnonRateThrottle, WorkingHoursRateThrottle,)
    throttle_scope = 'low_request'
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name',)
    ordering_fields = ('name', 'birth_year') 
    ordering = ('birth_year',) 

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
    # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
