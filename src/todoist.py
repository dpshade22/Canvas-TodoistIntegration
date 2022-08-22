import requests, json
from todoist_api_python.api import TodoistAPI
import random
from datetime import datetime, timezone
from dotenv import load_dotenv


load_dotenv()


class Todoist:
    def __init__(self, api, todoistKey):
        self.api = api
        self.todoistKey = todoistKey

    def addNewTasks(self, taskName, taskClass, currTasks, dueDate=None, url=None):
        task = f"{taskClass}: {taskName}"

        # Conditional Skips
        if "LIVE" in taskName:
            return

        url = "https://api.todoist.com/sync/v9/completed/get_all"

        payload = ""
        headers = {
            "cookie": "csrf=8af57fcfdde54dc3b650bc3d251c47b5",
            "Authorization": f"Bearer {self.todoistKey}",
        }

        res = requests.request("GET", url, data=payload, headers=headers).json()

        for item in res["items"]:
            if task in item["content"]:
                print(f"Skipped {task}, since it's already been completed")
                return

        labelDict = self.api.get_labels()
        taskDict = self.api.get_tasks()

        labelDict = {label.name: label.id for label in labelDict}
        taskIDS = {task.content: task.id for task in taskDict}

        # Creates label if it doesn't exist
        if taskClass not in labelDict.keys():
            label = self.api.add_label(
                name=taskClass, color=random.choice(range(30, 50))
            )
            labelDict[taskClass] = label.id

        # If task is already created, update, or skip it
        currTaskID = taskIDS.get(f"{taskClass}: {taskName}")
        if currTaskID:
            oldDue = (
                self.api.get_task(task_id=currTaskID).due.datetime
                if self.api.get_task(task_id=currTaskID).due is not None
                else "2001-01-01T00:00:00"
            )

            if oldDue and "Z" not in oldDue:
                oldDue = (
                    datetime.strptime(oldDue, "%Y-%m-%dT%H:%M:%S")
                    .astimezone(timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ")
                )

            if task in taskIDS.keys() and oldDue != dueDate:
                task = self.api.update_task(task_id=currTaskID, due_string=dueDate)
                print(f"Successfully updated: {taskClass}: {taskName}")
                return
            elif task in taskIDS.keys() and oldDue == dueDate:
                print(f"Skipped {task} since it's already created")
                return

        # Try to add the task
        try:
            task = self.api.add_task(
                content=task,
                due_string=dueDate,
                label_ids=[labelDict[taskClass]],
                description=f"[Canvas link]({url})",
            )
            print(f"Successfully added: {task.content}")
        except Exception as error:
            print(error)
