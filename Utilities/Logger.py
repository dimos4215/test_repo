import time

class Logger:

    def __init__(self):
        print('=====LOG START=====')

        self.task = ''
        self.str_time = 0
        self.end_time = 0
        self.task_map = {}

        self.metric=''
        self.metric_map = {}


    def log_task(self,task_name):

        if self.task == '':
            self.task = task_name
            self.str_time = time.clock()

        else:
            self.end_time = time.clock()
            self.task_map [self.task] = 'Duration: ' + str(self.end_time-self.str_time)
            self.task = task_name
            self.str_time = time.clock()


    def log_metric(self,metric,value):

        if metric in self.metric_map:
            self.metric_map[metric] = [value]
        else:
            self.metric_map[metric].append(value)


    def end(self):
        self.end_time = time.clock()
        self.task_map[self.task] = 'Duration: ' + str(self.end_time - self.str_time)

        fp = open(dir, "a")