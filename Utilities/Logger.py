import time
import os


class Logger:

    def __init__(self,config_obj):
        print('=====LOG START=====')

        self.task = ''
        self.str_time = 0
        self.end_time = 0
        self.task_map = {}
        self.static_metric_map = {}
        self.dynamic_metric_map = {}
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


    def log_static_metric(self, metric, value):
        if metric not in self.static_metric_map:
            self.static_metric_map[metric] = [value]
        else:
            self.static_metric_map[metric].append(value)


    def log_dynamic_metric(self, metric, metric_key,value):
        if metric not in self.dynamic_metric_map:
            self.dynamic_metric_map[metric] = {}
            self.dynamic_metric_map[metric][metric_key] = value
        else:
            if metric_key not in self.dynamic_metric_map[metric]:
                self.dynamic_metric_map[metric][metric_key] = value
            else:
                self.dynamic_metric_map[metric][metric_key] = value


    def end(self):
        self.end_time = time.clock()
        self.task_map[self.task] = ' Duration: ' + str(self.end_time - self.str_time)

        res_separator = '\n\n====================================================\n'
        if os.path.exists(self.log_dir):
            os.remove(self.log_dir)


        f = open(self.log_dir, "a")

        #f.write(self.config_obj)# write configs settings

        for task in self.task_map:
            f.write(task + self.task_map[task]+'\n')

        for metric in self.static_metric_map:
            f.write(res_separator+metric+'\n')

            for value in self.static_metric_map[metric]:
                f.write(str(value)+'\n')

        print('self.dynamic_metric_map',self.dynamic_metric_map)
        rowformat='{},{}\n'
        for metric in self.dynamic_metric_map:

            f.write(res_separator+metric+'\n')

            for metrickey in self.dynamic_metric_map[metric]:
                value = self.dynamic_metric_map[metric][metrickey]
                f.write(str(metrickey)+','+str(value)+'\n')
