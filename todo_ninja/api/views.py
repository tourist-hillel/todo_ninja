# from ninja import Router
# from django.shortcuts import get_object_or_404
# from api.models import Task
# from api.schemas import TaskIn, TaskOut, ErrorResponse
# from ninja.errors import HttpError
# from typing import List


# router = Router(tags=['ToDoApp'])


# @router.get(
#     path='/tasks',
#     response=List[TaskOut],
#     summary='All tasks',
#     description='Retrieve a list of all task items'
# )
# def list_tasks(request):
#     return Task.objects.all()


# @router.get(
#     path='/tasks/{task_id}',
#     response=TaskOut
# )
# def get_task(request, task_id: int):
#     task = get_object_or_404(Task, id=task_id)
#     return task

# @router.post(
#     '/tasks',
#     response={201: TaskOut}
# )
# def create_task(request, payload: TaskIn):
#     task = Task.objects.create(**payload.dict())
#     return task


# @router.put(
#     path='/tasks/{task_id}',
#     response=TaskOut
# )
# def update_task(request, task_id: int, payload: TaskIn):
#     task = get_object_or_404(Task, id=task_id)
#     for attr, value in payload.dict().items():
#         setattr(task, attr, value)
#     task.save()
#     return task


# @router.delete(
#     path='/tasks/{task_id}',
#     response={204: None}
# )
# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     task.delete()
#     return 204, None
