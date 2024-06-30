import os
import requests
import json


class CommandExecutor:
    version = '3.10.1 By CanFeng'

    def __init__(self):
        self.commands = {}

    def _version(self):
        return self.version

    def add_command(self, command_name, function):
        import Server
        if command_name not in self.commands:
            self.commands[command_name] = function
            Server.output_log(f"Command '{command_name}' added successfully.")
        else:
            Server.output_log(f"Command '{command_name}' already exists.")

    def display_help(self, command=None):
        if command:
            help_text = self.commands.get(command, lambda: "Command not found")()
            print(help_text)
        else:
            print("Available commands:")
            for cmd in self.commands.keys():
                print(f"- {cmd}")

    def execute_command(self, command_name, *args):
        import Server
        if command_name in self.commands:
            Server.output_log(f'Run Command {self.commands[command_name]}')
            result = self.commands[command_name](*args)
            try:
                for i in result:
                    Server.output_log(i)
            except:
                Server.output_log(result)
        else:
            Server.output_log(f'Cannot Run Command {command_name}')
