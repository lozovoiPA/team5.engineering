import os

import win32com.client
import pythoncom
from datetime import datetime, timedelta


class TaskScheduler:
    def __init__(self, exe_path, working_dir, script_path=None):
        pythoncom.CoInitialize()
        self.scheduler = win32com.client.Dispatch('Schedule.Service')
        self.scheduler.Connect()
        self.root_folder = self.scheduler.GetFolder('\\')

        self.exe_path = exe_path
        self.script_path = script_path
        self.working_dir = working_dir

    def create_notification_task(self, task_name, run_time, script_args):
        task_definition = self.scheduler.NewTask(0)

        reg_info = task_definition.RegistrationInfo
        reg_info.Description = f"Notifications for meetings made in Smartmeet application."
        reg_info.Author = "Smartmeet"

        principal = task_definition.Principal
        principal.LogonType = 3
        principal.RunLevel = 0

        settings = task_definition.Settings
        settings.Enabled = True
        settings.StartWhenAvailable = True
        settings.Hidden = False

        trigger = task_definition.Triggers.Create(1)
        start_boundary = run_time.isoformat()
        trigger.StartBoundary = start_boundary

        action = task_definition.Actions.Create(0)
        action.Path = self.exe_path
        action.Arguments = script_args if self.script_path is None else f"{self.script_path} {script_args}"
        action.WorkingDirectory = self.working_dir

        self.root_folder.RegisterTaskDefinition(
            task_name,
            task_definition,
            6,
            None,
            None,
            3,
            None
        )

        print(f"Task '{task_name}' created for {run_time}")

    def cancel_task(self, task_name):
        try:
            self.root_folder.DeleteTask(task_name, 0)
            print(f"Task '{task_name}' cancelled")
            return True
        except Exception as e:
            print(f"Error cancelling task: {e}")
            return False

    def postpone_task(self, task_name, new_time: datetime):
        try:
            task = self.root_folder.GetTask(task_name)
            task_definition = task.Definition
            trigger = task_definition.Triggers[0]
            trigger.StartBoundary = new_time.isoformat()
            self.root_folder.RegisterTaskDefinition(
                task_name,
                task_definition,
                6,
                None,
                None,
                3,
                None
            )
            print(f"Task '{task_name}' postponed to {new_time}")
            return True
        except Exception as e:
            print(f"Error postponing task: {e}")
            return False

    def list_tasks(self):
        tasks = self.root_folder.GetTasks(0)
        task_list = []
        for task in tasks:
            if task.Name.startswith("Notification_"):
                task_list.append({
                    'name': task.Name,
                    'next_run': task.NextRunTime,
                    'status': task.State
                })
        return task_list
