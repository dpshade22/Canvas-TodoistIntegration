import requests, json
from todoist_api_python.api import TodoistAPI
import random
from datetime import datetime, timezone
import pytz


class Todoist:
    def __init__(self, api):
        self.api = api

    def addNewTasks(self, taskName, taskClass, currTasks, dueDate=None, url=None):
        # Conditional Skips
        if "LIVE" in taskName:
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

        currTaskID = taskIDS.get(f"{taskClass}: {taskName}")
        if currTaskID:
            oldDue = (
                self.api.get_task(task_id=currTaskID).due.datetime
                if self.api.get_task(task_id=currTaskID).due is not None
                else "2001-01-01T00:00:00"
            )

            if "Z" not in oldDue:
                oldDue = (
                    datetime.strptime(oldDue, "%Y-%m-%dT%H:%M:%S")
                    .astimezone(timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ")
                )

            if f"{taskClass}: {taskName}" in taskIDS.keys() and oldDue != dueDate:
                task = self.api.update_task(task_id=currTaskID, due_string=dueDate)
                print(f"Successfully updated: {taskClass}: {taskName}")
                return
            elif f"{taskClass}: {taskName}" in taskIDS.keys() and oldDue == dueDate:
                return

        try:
            task = self.api.add_task(
                content=f"{taskClass}: {taskName}",
                due_string=dueDate,
                label_ids=[labelDict[taskClass]],
                description=f"[Canvas link]({url})",
            )
            print(f"Successfully added: {task.content}")
        except Exception as error:
            print(error)
