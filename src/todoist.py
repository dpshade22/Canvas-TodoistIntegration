import requests, json
from todoist_api_python.api import TodoistAPI
import random
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import pytz

load_dotenv()


class Todoist:
    def __init__(self, api, todoistKey, labelDict, taskDict):
        self.api = api
        self.todoistKey = todoistKey
        self.labelDict = labelDict
        self.taskDict = taskDict

    def addNewTasks(self, taskName, taskClass, dueDate=None, url=None):
        task = f"{taskClass}: {taskName}"
        newUrl = f"[Canvas link]({url})"

        # Conditional Skips
        if "LIVE" in taskName:
            return

        completedTasks = "https://api.todoist.com/sync/v9/completed/get_all"

        payload = ""
        headers = {
            "cookie": "csrf=8af57fcfdde54dc3b650bc3d251c47b5",
            "Authorization": f"Bearer {self.todoistKey}",
        }

        res = requests.request(
            "GET", completedTasks, data=payload, headers=headers
        ).json()

        for item in res["items"]:
            if task in item["content"]:
                print(f"Skipped {task}, since it's already been completed")
                return

        labelDict = {label.name: label.id for label in self.labelDict}
        taskIDS = {task.content: [task.id, task.description] for task in self.taskDict}

        # Creates label if it doesn't exist
        if taskClass not in labelDict.keys():
            label = self.api.add_label(
                name=taskClass, color=random.choice(range(30, 50))
            )
            labelDict[taskClass] = label.id

        # If task is already created, update, or skip it
        currTaskID, oldUrl = taskIDS.get(task) if taskIDS.get(task) != None else [None, None]
        allDesc = [task[1] for task in taskIDS.values()]

        if currTaskID:
            taskObj = self.api.get_task(task_id=currTaskID).due
            oldDue = None
          
            if taskObj:
                if "Z" in taskObj.datetime:
                    oldDue = taskObj.datetime 
                elif "Z" in taskObj.string: 
                    oldDue = taskObj.string
            else:
                oldDue = "No date"
        
            if oldDue != dueDate or newUrl not in allDesc:
                taskUpdated = self.api.update_task(
                    task_id=currTaskID,
                    due_string=dueDate,
                    description=newUrl,
                )
                print(f"Successfully updated: {task}")

            elif oldDue == dueDate:
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
