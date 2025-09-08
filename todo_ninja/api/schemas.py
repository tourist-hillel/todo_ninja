from ninja import ModelSchema, Schema
from api.models import Task
from datetime import datetime


class TaskIn(ModelSchema):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_completed']


class TaskOut(ModelSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Meta:
        model = Task
        fields = '__all__'

class ErrorResponse(Schema):
    detail: str
