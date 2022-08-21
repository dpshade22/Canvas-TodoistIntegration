import requests, json
from todoist_api_python.api import TodoistAPI
import random


class Todoist:
    def __init__(self, api):
        self.api = api

    def addNewTasks(self, taskName, taskClass, currTasks, dueDate=None, url=None):
        labelDict = self.api.get_labels()
        labelDict = {label.name: label.id for label in labelDict}

        # Creates label if it doesn't exist
        if taskClass not in labelDict.keys():
            label = self.api.add_label(
                name=taskClass, color=random.choice(range(30, 50))
            )
            labelDict[taskClass] = label.id

        if f"{taskClass}: {taskName}" in [task.content for task in currTasks]:
            return

        try:
            task = self.api.add_task(
                content=f"{taskClass}: {taskName}",
                due_string=dueDate,
                label_ids=[labelDict[taskClass]],
                description=f"[Canvas link]({url})",
            )
            print(task)
        except Exception as error:
            print(error)
