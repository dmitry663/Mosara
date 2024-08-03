import os
import subprocess
import threading

from utils import read_json_file, DotDict

replacement_list = read_json_file("condition_replacement_list.json")

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

         
        self.modify_commands()
        self.command = " ".join(self.command_list)
        
        self.thread = threading.Thread(target = self.run_command) 
        
    def modify_commands(self):
        check_list = []
        for condition in replacement_list["conditions"]:
            if "super" in condition["condition"] and not self.super:
                continue
            if "not super" in condition["condition"] and self.super:
                continue
            if "windows" in condition["condition"] and not self.iswindows:
                continue
            if "not windows" in condition["condition"] and self.iswindows:
                continue

            for arg in condition["args"]:
                if arg["original_argument"] in self.command_list and arg["original_argument"] in check_list:
                    check_list.append(arg["original_argument"])
                    self.command_list = [arg["replacement_argument"] if arg["original_argument"] else argx == arg["original_argument"] for argx in self.command_list]

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
