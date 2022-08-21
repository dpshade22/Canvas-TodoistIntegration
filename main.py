import os
import datetime as datetime
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv

from src.canvas import CanvasApi
from src.todoist import Todoist

load_dotenv()

todoistKey = os.environ.get("todoistKey")
canvasKey = os.environ.get("canvasKey")

canvasProfile = CanvasApi(canvasKey, "uk")
todoistAPI = TodoistAPI(todoistKey)
myAPI = Todoist(todoistAPI)


def addTasks(courseList):
    canvasProfile.set_courses_and_id()
    currTasks = todoistAPI.get_tasks()
    due = ""
    for course in courseList:
        for assignment in canvasProfile.get_assignment_objects(course.name, "future"):
            myAPI.addNewTasks(
                assignment["name"],
                course.name,
                currTasks,
                dueDate=assignment["due_at"],
                url=assignment["url"],
            )


addTasks(canvasProfile.get_courses_within_six_months())
