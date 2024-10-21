from datetime import datetime
import time
import random
from threading import Lock

class LogServer:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LogServer, cls).__new__(cls)
                cls._instance.log_entries = []
            return cls._instance

    def start_log(self, process_id, start_time):
        self.log_entries.append((process_id, start_time, None))

    def end_log(self, process_id, end_time):
        for i, entry in enumerate(self.log_entries):
            if entry[0] == process_id:
                self.log_entries[i] = (process_id, entry[1], end_time)
                break
        
        self.sort_and_write_to_file()

    def sort_and_write_to_file(self):
        sorted_entries = sorted(self.log_entries, key=lambda x: x[1])  # Sort by start_time
        with open("process_logs.txt", "w") as f:
            for entry in sorted_entries:
                process_id, start_time, end_time = entry
                f.write(f"Process ID: {process_id}, Start Time: {start_time}, End Time: {end_time if end_time else 'Still running'}\n")

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.start_time = None
        self.end_time = None

    def start_function(self):
        self.start_time = datetime.now()
        
        LogServer().start_log(self.process_id, self.start_time)

    def end_function(self):        
        self.end_time = datetime.now()
        LogServer().end_log(self.process_id, self.end_time)
