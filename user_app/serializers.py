from rest_framework import serializers
from .models import User, Role, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name"]


class RoleSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer

    class Meta:
        model = Role
        fields = ["id", "name", "organization"]


class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "organization", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # No need to pop 'role' and 'organization', since they are already primary key fields
        role = validated_data.pop("role")
        organization = validated_data.pop("organization")

        # Create the user
        user = User.objects.create_user(
            role=role, organization=organization, **validated_data
        )
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data["password"])  # Hash password
            validated_data.pop(
                "password"
            )  # Remove password from validated data to avoid overwriting
        if "role" in validated_data:
            instance.role = validated_data.pop("role")
        if "organization" in validated_data:
            instance.organization = validated_data.pop("organization")

        return super().update(instance, validated_data)
