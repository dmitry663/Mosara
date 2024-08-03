import os
import subprocess
import threading

from utils import read_json_file, DotDict

class Command:
    def __init__(self, app_data):
        self.name = app_data.name
        self.executable = app_data.executable
        self.args = app_data.args
        self.super = app_data.super

        if os.name == 'nt':
            self.iswindows = True
        else:
            self.iswindows = False
        
        self.command_list = []

        if not self.iswindows and self.super:
            self.command_list.append("sudo")
        self.command_list.append(self.executable)
        self.command_list.extend(self.args)

        self.command_list = [arg for arg in self.command_list]
        self.command = " ".join(self.command_list)
        
        self.thread = threading.Thread(target = self.run_command) 
        
    def get_command(self):
        return self.command
    
    def run_command(self):
        subprocess.run(self.command, shell=True)

    def run_command_threading(self):
        self.thread.start()
        
if __name__ == "__main__":
    config_data = read_json_file("sample.json")
    print(config_data)
    command = Command(DotDict(config_data["apps"][0]))

    command.run_command()
