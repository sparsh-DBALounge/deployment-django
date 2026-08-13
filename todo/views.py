import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from .models import Todo, PriorityChoices
from django.views.decorators.csrf import csrf_exempt

def not_found(todo_id):
    return JsonResponse(
        {   
            "status": "error",
            "message": f"Todo with ID: {todo_id} does not exist"
        },
        status=404
    )

@csrf_exempt
def todos_view(request):
    if request.method == "GET":
        todos = Todo.objects.all().values()
        todos_list = list(todos)

        return JsonResponse(
            {
                "todos_count": len(todos_list),
                "todos": todos_list 
            },
            status=200
        )

    if request.method == "POST":
        payload = json.loads(request.body)

        todo = Todo(
            title = payload.get("title"),
            description = payload.get("description", ""),
            priority = payload.get("priortiy", PriorityChoices.LOW),
            deadline = payload.get("deadline", None),
            user_id = payload.get("user_id")
        )
        todo.save()

        return JsonResponse(
            {"message": "Todo created successfully"},
            status=201
        )


    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def todo_view(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        return not_found(todo_id)
        
    if request.method == "GET":
        data = {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "priority": todo.priority,
            "deadline": todo.deadline,
            "user_id": todo.user_id,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at,
        }
        if not todo:
            return not_found(todo_id)

        return JsonResponse(data, status=200) 

    if request.method == "DELETE":
        todo.delete()
        return HttpResponse(status=204)

    if request.method == "PUT":
        todo = todo
        payload = json.loads(request.body)

        todo.title = payload.get("title", todo.title)
        todo.description = payload.get("description", todo.description)
        todo.priority = payload.get("priority", todo.priority)
        todo.deadline = payload.get("deadline", todo.deadline)

        todo.save()
        return JsonResponse(
            {"message": f"Todo with ID: {todo_id} updated successfully"},
            status=200
        )

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])