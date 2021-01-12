from classes.platform import Platform
from classes.user import User


platform = Platform()

simeon = platform.create_user("Simeon")
client = simeon.create_client("Visa")
client.create_project("Summer promo")
simeon.create_client("Kamenitza").create_project("RGB promo").create_task("Do design!")

boris = platform.create_user("Boris")
boris.create_client("HP")

for user in Platform.all_users:
    print(f"Name: {user.name}")
    for client in user.clients:
        print(f"-Client: {client.name}")
        for project in client.projects:
            print(f"--Project: {project.name}")
            for task in project.tasks:
                print(f"---Task: {task.name}")

for user in Platform.all_users:
    print(user.name)
print(User.all_clients)