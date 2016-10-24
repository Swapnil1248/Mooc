from datetime import datetime
class Course:
    def __init__(self, course_id):
        self.course_id = course_id
        self.children = []
        self.moduleCounts = {}
    def addChild(self, node):
        self.children.append(node)
    def addModuleCount(self, category):
        if(category not in self.moduleCounts):
            self.moduleCounts[category] = 0
        self.moduleCounts[category] += 1
    def setDate(self, start, end):
        self.start = datetime.strptime(start, "%Y-%m-%d")
        self.end = datetime.strptime(end, "%Y-%m-%d")
    def getDay(self, date):
        activity_date = datetime.strptime(date, "%Y-%m-%d")
        return (activity_date - self.start).days + 1
    def __str__(self):
        return self.course_id