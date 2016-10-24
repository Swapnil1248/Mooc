from datetime import datetime

class Module:
    def __init__(self, line):
        a = line.strip().split(",")
        self.course_id = a[0]
        self.module_id = a[1]
        self.category = a[2]
        if (len(a[3].strip()) != 0):
            self.children = a[3].strip().split(" ")
        else:
            self.children = []
        if (a[4] != "null"):
            self.start = datetime.strptime(a[4], '%Y-%m-%dT%H:%M:%S')
        else:
            self.start = None
        self.parent = None
        self.children_nodes = []
    def __str__(self):
        return 'course_id: ' + self.course_id + ', module_id: ' + self.module_id + ', category: ' + self.category