import os
import datetime as datetime
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv

from src.canvas import CanvasApi
from src.todoist import Todoist

load_dotenv()


def addTasks(canvasKey, todoistKey):
    canvasProfile = CanvasApi(canvasKey, "uk")
    todoistAPI = TodoistAPI(todoistKey)
    todoistClass = Todoist(todoistAPI, todoistKey)

    canvasProfile.set_courses_and_id()
    currTasks = todoistAPI.get_tasks()

    for course in canvasProfile.get_courses_within_six_months():
        for assignment in canvasProfile.get_assignment_objects(course.name, "future"):
            todoistClass.addNewTasks(
                assignment["name"],
                course.name,
                dueDate=assignment["due_at"],
                url=assignment["url"],
            )


dpsTodoistKey = os.environ.get("dpsTodoistKey")
dpsCanvasKey = os.environ.get("dpsCanvasKey")

# agbTodoistKey = os.environ.get("agbTodoistKey")
# agbCanvasKey = os.environ.get("agbCanvasKey")

addTasks(dpsCanvasKey, dpsTodoistKey)
# addTasks(agbCanvasKey, agbTodoistKey)
