from fastapi import APIRouter, HTTPException, Depends
from models.todo import Todo
from database import create_todo, delete_todo, get_all_todos, update_todo, check_id
from dependencies import get_current_user

todo_router = APIRouter()


@todo_router.get("/")
def get_todos(user_id: int = Depends(get_current_user)):
    return get_all_todos(user_id)


@todo_router.post("/")
def c_todo(todo: Todo, user_id: int = Depends(get_current_user)):
    res = todo.model_dump()
    create_todo(res["task"], res["done"], res["created_at"], user_id)
    return {"message": "Todo created", "todo": res}


@todo_router.delete("/{id}")
def d_todo(id: int, user_id: int = Depends(get_current_user)):
    if not check_id(id):
        raise HTTPException(status_code=404, detail="id doesn't exists")
    delete_todo(id)
    return {"message": "deleted successfully"}


@todo_router.put("/{id}")
def u_todo(id: int, todo: Todo, user_id: int = Depends(get_current_user)):
    if not check_id(id):
        raise HTTPException(status_code=404, detail="id doesn't exists")
    update_todo(id, todo.task, todo.done)
    return {"message": "updated successfully"}
