from locust import HttpUser, TaskSet, task, between


class WebsiteUser(HttpUser):
    wait_time = between(0.001, 0.005)

    @task(1)
    def index(self):
        endpoint_url = "http://django:8123/categories/MLA5726"
        self.client.get(endpoint_url)

    def on_start(self):
        pass
