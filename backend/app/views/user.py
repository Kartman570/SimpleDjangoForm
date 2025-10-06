from rest_framework import viewsets
from rest_framework.response import Response

from app.models import User
from app.serializers import UserSerializer

FAKE_DB = {}
NEXT_ID = 1


class UserViewSet(viewsets.ModelViewSet):
    # mock and overwrite most of a class, because there is no DB
    serializer_class = UserSerializer
    queryset = User.objects.none()

    def list(self, request):
        return Response(list(FAKE_DB.values()))

    def retrieve(self, request, pk=None):
        pk = int(pk)
        user = FAKE_DB.get(pk)
        if not user:
            return Response({"detail": "Not found."}, status=404)
        return Response(user)

    def create(self, request):
        global NEXT_ID #  noqa: PLW0603
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = {"id": NEXT_ID, **serializer.validated_data}
        FAKE_DB[NEXT_ID] = user_data
        NEXT_ID += 1

        print(f'---API_LOGS---Submit new user via API:\n{user_data}')
        return Response(user_data, status=201)

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = int(pk)
        if pk not in FAKE_DB:
            return Response({"detail": "Not found."}, status=404)

        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        FAKE_DB[pk].update(serializer.validated_data)
        print(f'---API_LOGS---Update user data via PATCH/PUT:\n{request.data}')
        return Response(FAKE_DB[pk])

    def destroy(self, request, pk=None):
        pk = int(pk)
        if pk in FAKE_DB:
            del FAKE_DB[pk]
            print(f'---API_LOGS---Successfully delete user:\nid={pk}')
            return Response(status=204)
        return Response({"detail": "Not found."}, status=404)
