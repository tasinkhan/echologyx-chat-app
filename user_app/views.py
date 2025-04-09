from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role, Organization, User
from .serializers import RoleSerializer, OrganizationSerializer, UserSerializer

# Create your views here.


class OrganizationBulkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # The incoming data is expected to be a list of dictionaries
        many = isinstance(request.data, list)
        print("===the value of many====", many)
        serializer = OrganizationSerializer(data=request.data, many=many)

        if serializer.is_valid():
            # Collect the objects to be bulk created
            if many:
                # Collect the organizations to be bulk created
                organizations = [
                    Organization(**validated_data)
                    for validated_data in serializer.validated_data
                ]
                Organization.objects.bulk_create(organizations)
                return Response(
                    {"detail": "Organizations created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                Organization.objects.create(**serializer.validated_data)
                return Response(
                    {"detail": "Organization created successfully."},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleBulkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # The incoming data is expected to be a list of dictionaries
        many = isinstance(request.data, list)
        print("===the value of many====", many)
        serializer = RoleSerializer(data=request.data, many=many)

        if serializer.is_valid():
            # Collect the objects to be bulk created
            if many:
                # Collect the roles to be bulk created
                roles = [
                    Role(**validated_data)
                    for validated_data in serializer.validated_data
                ]
                Role.objects.bulk_create(roles)
                return Response(
                    {"detail": "roles created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                Role.objects.create(**serializer.validated_data)
                return Response(
                    {"detail": "Role created successfully."},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBulkCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # The incoming data is expected to be a list of dictionaries
        many = isinstance(request.data, list)

        # Initialize the User serializer with the data
        serializer = UserSerializer(data=request.data, many=many)

        if serializer.is_valid():
            # Collect the users to be bulk created
            users_to_create = []
            print("1")
            if many:
                for validated_data in serializer.validated_data:
                    role = validated_data["role"]
                    organization = validated_data["organization"]

                    # Create the User instance
                    user_instance = User(
                        username=validated_data["username"],
                        email=validated_data["email"],
                        role=role,
                        organization=organization,
                        password=validated_data["password"],
                    )
                    users_to_create.append(user_instance)

                # Bulk create the users
                User.objects.bulk_create(users_to_create)
                return Response(
                    {"detail": "Users created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                # Create a single user if not many
                User.objects.create(**serializer.validated_data)
                return Response(
                    {"detail": "User created successfully."},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
