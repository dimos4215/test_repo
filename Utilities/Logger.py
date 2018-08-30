import time

class Logger:

    def __init__(self,config_obj):
        print('=====LOG START=====')

        self.task = ''
        self.str_time = 0
        self.end_time = 0
        self.task_map = {}
        self.metric_map = {}
        self.log_dir=config_obj.log_dir
        self.config_obj=config_obj


    def log_task(self,task_name):

        if self.task == '':
            self.task = task_name
            self.str_time = time.clock()

        else:
            self.end_time = time.clock()
            res = ' Duration: ' + str(self.end_time-self.str_time)
            self.task_map [self.task] = res
            print(self.task+res)
            self.task = task_name
            self.str_time = time.clock()


    def log_metric(self,metric,value):


        if metric not in self.metric_map:
            self.metric_map[metric] = [value]
        else:
            self.metric_map[metric].append(value)


    def end(self):
        self.end_time = time.clock()
        self.task_map[self.task] = ' Duration: ' + str(self.end_time - self.str_time)

        res_separator = '\n\n====================================================\n'
        f = open(self.log_dir, "a")

        #f.write(self.config_obj)# write configs settings

        for task in self.task_map:
            f.write(task + self.task_map[task]+'\n')

        for metric in self.metric_map:
            f.write(res_separator+metric+'\n')

            for value in self.metric_map[metric]:
                f.write(str(value)+'\n')