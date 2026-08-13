import json
from django.http import  JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

def not_found(user_id):
    return JsonResponse(
        {"status": "error",
        "message": f"user with ID: {user_id} does not exist"
        },
        status=404
    )

@csrf_exempt
def users_view(request):
    if request.method == "GET":
        users = User.objects.all().values()
        users_list = list(users)
        return JsonResponse(
            {
                "users_count": len(users_list),
                "users": users_list
            },
            status=200
        )


    if request.method == "POST":
        payload = json.loads(request.body)

        email = payload.get('email')
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            return JsonResponse(
                        {"message": f"User with email {email} already exists"},
                        status=409
                )

        user = User(
            name = payload.get('name'),
            email = email,
            age = payload.get('age')
        )

        user.save()
        return JsonResponse(
            {"message": "New user created successfully"},
            status=201
        )

    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return not_found(user_id)

    if request.method == "GET":
        print(user.todos)
        data = {
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "todos_count": len(list(user.todos.all().values()))
        }

        return JsonResponse(data, status=200)

    if request.method == 'PUT':
        payload = json.loads(request.body)
        user.name = payload.get("name", user.name)
        user.email = payload.get("email", user.email)
        user.age = payload.get("age", user.age)

        user.save()

        return JsonResponse(
            {"message": f"User with ID: {user_id} updated successfuly"},
            status = 200
        )

    if request.method == "DELETE":
        user.delete()
        return HttpResponse(status=204)

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

@csrf_exempt
def get_user_todos(request, user_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return not_found(user_id)

    todos_list = list(user.todos.all().values())
    return JsonResponse(todos_list, safe=False)