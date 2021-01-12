from classes.task import Task


class Project:

    all_tasks = []

    def __init__(self, name):
        self.name = name
        self.tasks = []

    def create_task(self, name):
        task = Task(name)
        self.tasks.append(task)
        self.all_tasks.append(task)
        return task