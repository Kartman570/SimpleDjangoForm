"""
Since that test project require no DB, all data oriented actions are performed with file variable.
Because of that, we rewrite all methods inside viewset into static methods.
Overall structure of modelviewset remains close to what it should be
"""
from rest_framework import viewsets
from rest_framework.response import Response

from app.models import User
from app.serializers import UserSerializer

FAKE_DB = {}
NEXT_ID = 1


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for user CRUD operations.
    Django from the box already can handle main CRUD ops.
    But we use fake DB variable, so we need to rewrite all methods inside.
    No filtering or permission checks right now
    """
    serializer_class = UserSerializer
    queryset = User.objects.none()

    @staticmethod
    def list(request):
        """GET viewset for retrieve all available users in fake DB variable"""
        return Response(list(FAKE_DB.values()))

    @staticmethod
    def retrieve(request, pk=None):
        """GET viewset for retrieve specific user by id in fake DB variable"""
        pk = int(pk)
        user = FAKE_DB.get(pk)
        if not user:
            return Response({"detail": "Not found."}, status=404)
        return Response(user)

    def create(self, request):
        """POST viewset creates new user record in fake DB variable"""
        global NEXT_ID #  noqa: PLW0603
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = {"id": NEXT_ID, **serializer.validated_data}
        FAKE_DB[NEXT_ID] = user_data
        NEXT_ID += 1

        print(f'---API_LOGS---Submit new user via API:\n{user_data}')
        return Response(user_data, status=201)

    def update(self, request, pk=None, *args, **kwargs):
        """PUT/PATCH viewset to update user record in fake DB variable"""
        partial = kwargs.pop('partial', False)
        pk = int(pk)
        if pk not in FAKE_DB:
            return Response({"detail": "Not found."}, status=404)

        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        FAKE_DB[pk].update(serializer.validated_data)
        print(f'---API_LOGS---Update user data via PATCH/PUT:\n{request.data}')
        return Response(FAKE_DB[pk])

    @staticmethod
    def destroy(request, pk=None):
        """DELETE viewset to remove specific user record by id from fake DB variable"""
        pk = int(pk)
        if pk in FAKE_DB:
            del FAKE_DB[pk]
            print(f'---API_LOGS---Successfully delete user:\nid={pk}')
            return Response(status=204)
        return Response({"detail": "Not found."}, status=404)
