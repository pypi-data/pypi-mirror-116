import datetime as dt
import pandas as pd
import numpy as np
import threading
import time
import os

#load other scripts
from . import dash_tools as dash
from . import json_tools as json
from . import dictionary_tools as dictionary

__version__ = "1.5.4"

#print command with Script name in front
class ScriptPrint:
    def __init__(self, name, block = False, log = False):
        self.name = name
        self.block = block
        self.log = log
        self.logfile = "output.log"
        self.logrange = dt.timedelta(days = 1)
        self.logtimeformat = "%d_%m_%Y %H:%M:%S.%f"
        self.loglist = {}
        self.running = True
        self.thread = threading.Thread(target=self.__log_thread__)
        self.thread.start()
    def print(self, msg):
        if not self.block:
            print(f"[{self.name}]: {msg}")
        if self.log:
            self.loglist[dt.datetime.now().strftime(self.logtimeformat)] = msg
    def finish(self):
        self.running = False
    def __log_thread__(self):
        while True:
            if self.running:
                with open(self.logfile, "r") as rd:
                    loglines = np.array([l for l in rd.read().split("\n") if not l == ""])
                    del_logs = list()
                    for i,l in enumerate(loglines):
                        try:
                            cur_logtime = dt.datetime.strptime(l.split(" -> ")[0], self.logtimeformat)
                            if cur_logtime < dt.datetime.now() - self.logrange:
                                del_logs.append(i)
                        except:
                            del_logs.append(i)
                    loglines = np.delete(loglines, del_logs)
                    loglines = np.sort(loglines)
                    for ts, log in self.loglist.items():
                        log = str(log).replace('\n', ' ')
                        loglines = np.append(loglines, f"{ts} -> [{self.name}]: {log}")
                with open(self.logfile, "w") as wd:
                    wd.write("\n".join(loglines))
                self.loglist = {}
                time.sleep(1)
            else:
                break  
            
#Timer for Script runtimes
class Timer:
    def __init__(self):
        self.startpoint = None
        self.lapstartpoint = None
        self.runtime = dt.timedelta(seconds = 0)
        self.lapruntime = dt.timedelta(seconds = 0)
        self.laps = []
    def start(self):
        if not self.startpoint:
            self.startpoint = dt.datetime.now()
            self.lapstartpoint = dt.datetime.now()
        else:
            raise Exception("Timer already running")
    def pause(self):
        if self.startpoint:
            now = dt.datetime.now()
            self.runtime += now - self.startpoint
            self.lapruntime += now - self.lapstartpoint
            self.startpoint = None
            self.lapstartpoint = None
            return self.runtime
        else:
            raise Exception("Timer not running")
    def set_lap(self):
        if self.lapstartpoint:
            now = dt.datetime.now()
            self.laps.append(self.lapruntime + now - self.lapstartpoint)
            self.lapstartpoint = now
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
        else:
            self.laps.append(self.lapruntime)
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
    def get_runtime(self):
        if self.startpoint:
            return self.runtime + dt.datetime.now() - self.startpoint
        else:
            return self.runtime
    def get_laps(self):
        return self.laps
    def get_lap_runtime(self):
        if self.lapstartpoint:
            return self.lapruntime + dt.datetime.now() - self.lapstartpoint
        else:
            return self.lapruntime
    def reset(self):
        self.__init__()
timer = Timer()

#for getting variable name as string
def get_variable_name(var, namespace):
    if not isinstance(var, pd.DataFrame):
        return [k for k, v in namespace.items() if v == var][0]
    else:
        return [k for k, v in namespace.items() if var.equals(v)][0]