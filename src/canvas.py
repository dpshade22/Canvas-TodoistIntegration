import requests, json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class Class:
    def __init__(self, id=None, name=None, term_id=None, assignments=None):
        self.id = id
        self.name = name
        self.assignments = []
        self.term_id = term_id


# Class implementation of canvas API
class CanvasApi:
    def __init__(self, canvasKey, schoolAb=""):
        self.canvasKey = canvasKey
        self.schoolAb = schoolAb
        self.header = {"Authorization": "Bearer " + self.canvasKey}
        self.courses = {}

    def get_courses_within_six_months(self):
        
        url = f"https://{self.schoolAb}.instructure.com/api/v1/courses"
        
        querystring = {"per_page":"350"}
        
        payload = ""
        headers = {
            "cookie": "_csrf_token=1w3GGSY5y277Fr5m%252BxvP%252BBBxeYmmqY2fYM1mifSguCuya4l%252Bbk%252BGObB9%252BTKRKqaxdwAWpsWZyKgStSrrm%252FH3Yg%253D%253D; log_session_id=c86aaa6df20861f9eb9f187135c208c8; _legacy_normandy_session=AH4ltuqs4AitPXGvQJXlTw.zkdNmpMv8Zsb4nVkAMalIZKdYtrgygqeG8skrEhrcug95aURmCGyN58gPYLDWeHbc9XzMYnOZ_LqqaMgmmK_d4XhnL0ECVkgEo_Otm5nGiHvVOHhgIFfIURaHMe_IIJO.WIdaxvIl6w_YgYXfzqbnJxdmTbM.YwJ9zw; canvas_session=AH4ltuqs4AitPXGvQJXlTw.zkdNmpMv8Zsb4nVkAMalIZKdYtrgygqeG8skrEhrcug95aURmCGyN58gPYLDWeHbc9XzMYnOZ_LqqaMgmmK_d4XhnL0ECVkgEo_Otm5nGiHvVOHhgIFfIURaHMe_IIJO.WIdaxvIl6w_YgYXfzqbnJxdmTbM.YwJ9zw",
            "Authorization": f"Bearer {self.canvasKey}"
        }

        classes = []
        courses = requests.request("GET", url, data=payload, headers=headers, params=querystring).json()
        
        for course in courses:
          if course.get("name") != None and course.get("enrollment_term_id") == 10748:
              name = course.get("name")
              name = cleanCourseName(name)

              classObj = Class(
                  course.get("id"),
                  name,
                  course.get("enrollment_term_id"),
                  course.get("assignments"),
              )

              classes.append(classObj)

        return classes

    def get_all_courses(self):
        params = {
            "per_page": 200,
            "include": ["concluded"],
            "enrollment_state": ["active"],
        }
        readUrl = f"https://{self.schoolAb}.instructure.com/api/v1/courses"
        classes = []
        courses = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()

        for i in courses:
          if i.get("name") != None:
              name = i.get("name")
              name = cleanCourseName(name)

              classObj = Class(
                  i.get("id"),
                  name,
                  i.get("enrollment_term_id"),
                  i.get("assignments"),
              )
              classes.append(classObj)
      
        return classes

    # Initialize self.courses dictionary with the key being
    def set_courses_and_id(self):
        for courseObject in self.get_all_courses():
            if courseObject != None:
                self.courses[courseObject.name] = courseObject.id

    # Return a courses id number given the courses name
    def get_course_id(self, courseName):
        return self.courses[courseName]

    # Returns a list of all assignment objects for a given course
    def get_assignment_objects(self, courseName, timeframe=None):
        readUrl = f"https://{self.schoolAb}.instructure.com/api/v1/courses/{self.courses[courseName]}/assignments/"
        params = {"per_page": 500, "bucket": timeframe}

        assignments = requests.request(
            "GET", readUrl, headers=self.header, params=params
        ).json()
        assignmentList = []

        for assignment in assignments:
            if assignment.get("due_at") == None:
                assignment["due_at"] = "2021-01-01"

            assignment["url"] = assignment["html_url"]
            assignmentList.append(assignment)

        return assignmentList


    def list_classes_names(self):
        for course in self.get_course_objects():
            print(course.name)


def cleanCourseName(name):
    cleanName = ""
    num = 0

    if name != None:
        name = name.replace(" ", "")

    while name[num].isalpha() or name[num] == "/" or name[num] == "-":
        cleanName += name[num]

        if name[num] == name[-1]:
            break

        num += 1

    while name[num].isdigit() and num < 6:
        cleanName += name[num]

        if name[num] == name[-1]:
            break

        num += 1
    return cleanName
