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
            # Check if there is a time or not
            if (
                assignment["lock_at"] and assignment["due_at"]
            ) and datetime.datetime.strptime(
                assignment["lock_at"], "%Y-%m-%dT%H:%M:%SZ"
            ) > datetime.datetime.strptime(
                assignment["due_at"], "%Y-%m-%d"
            ):
                due = assignment["lock_at"]
            else:
                assignment["due_at"]

            # Add task to Todoist
            myAPI.addNewTasks(
                assignment["name"],
                course.name,
                currTasks,
                dueDate=due,
                url=assignment["html_url"],
            )


addTasks(canvasProfile.get_courses_within_six_months())
