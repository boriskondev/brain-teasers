from classes.project import Project


class Client:

    all_projects = []

    def __init__(self, name):
        self.name = name
        self.projects = []

    def create_project(self, name):
        project = Project(name)
        self.projects.append(project)
        self.all_projects.append(project)
        return project

    def __repr__(self):
        return self.name