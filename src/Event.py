from datetime import datetime

class Event:
    def __init__(self, line):
        words = line.strip().split(',')
        self.enrollment_id = int(words[0])
        self.time = datetime.strptime(words[1], '%Y-%m-%dT%H:%M:%S')
        self.source = words[2]
        self.event_type = words[3]
        self.module_id = words[4]
    def setCategory(self, object_map):
        if (object_map.has_key(self.module_id)):
            self.category = object_map[self.module_id].category
        else:
            self.category = 'UNKNOWN'
    def toKey(self):
        return '%s:%s:%s' % (self.source, self.event_type, self.category)
