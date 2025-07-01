from fastapi import FastAPI, HTTPException  # Importing FastAPI and HTTPException for creating the API and handling errors
from pydantic import BaseModel, Field  # Importing BaseModel for data validation and create object for post method
from enum import IntEnum
from typing import List, Optional

app = FastAPI()

class Priority(IntEnum):
    low = 3
    medium = 2
    high = 1
class ToDoBase(BaseModel):
    todo_name: str = Field(...,min_length=3,max_length=512,description='name of todo') # Using Field to set constraints on the todo_name
    priority: Priority = Field(default=Priority.low, description='Priority of the todo item')


class TodoCreate(ToDoBase):
    pass

class Todo(ToDoBase):
    todo_id: int = Field(..., description='Unique identifier for the todo item')  # Adding todo_id field to the Todo model which has todo_name and priority.. ToDoBase is inherited

    

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None,min_length=3,max_length=512,description='name of todo') # Using Field to set constraints on the todo_name
    priority: Optional[Priority] = Field(None, description='Priority of the todo item')
    #optional since everything is not required to update







all_todos =[
    Todo(todo_id=1,todo_name="sports",priority=Priority.high),
    Todo(todo_id=2,todo_name="art",priority=Priority.medium),  
    Todo(todo_id=3,todo_name="dance",priority=Priority.low),
    Todo(todo_id=4,todo_name="music",priority=Priority.high),
    Todo(todo_id=5,todo_name="reading",priority=Priority.medium)
]

@app.get("/")
def root():
    return {"Hello": "World"}

#query parameter just like /todos?todo_id=1
@app.get('/todos')
def get_todo_by_query(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
        
@app.get('/todos/{todo_id}',response_model=Todo)  # Path parameter just like /todos/1todo_name: str = Field(...,min_length=3,max_length=512,description='name of todo') # Using Field to set constraints on the todo_name
   

def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id== todo_id:
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")  # If todo not found, raise an HTTPException with a 404 status code and a detail message


@app.post('/todos', response_model=Todo)  # post method to create a new todo

def create_todo(todo: TodoCreate):
    new_id=max(todo.todo_id for todo in all_todos) +1
    new_todo=Todo(todo_id=new_id,
        todo_name = todo.todo_name,
        priority = todo.priority
    )
    all_todos.append(new_todo)
    return new_todo

# put( to update) ,delete
@app.put('/todos/{todo_id}',response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id==todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.priority is not None:   
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
        
@app.delete('/todos/{todo_id}',response_model=Todo)
def delete_todo(todo_id:int):
    for index,todo in enumerate(all_todos):
        if todo.todo_id==todo_id:
            deleted_todo=all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")

#use http exception to return error message which is string and response model is not todo

