from locust import HttpLocust, TaskSet, task

# skip


class UserTasks(TaskSet):

    @task
    def index(self):
        self.client.get("/")

    @task
    def stats(self):
        self.client.get("/stats/requests")


class WebsiteUser(HttpLocust):
    task_set = UserTasks
