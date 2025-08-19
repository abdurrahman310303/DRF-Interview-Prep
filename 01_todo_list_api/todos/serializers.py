from rest_framework import serializers
from .models import Todo
from users.serializers import UserSerializer


class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Todo
        fields = ['id','title','description','completed','due_date','created_at','updated_at','user']
        read_only_fields = ['created_at','updated_at','user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TodoToggleSerializer(serializers.ModelSerializer):
    completed = serializers.BooleanField()
