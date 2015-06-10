from locust import task

from marketing import MarketingTasks


class RSSTasks(MarketingTasks):
    """Locust tests related to RSS requests."""

    @task
    def show_feed_v1(self):
        """Simulate the retrieval of the course feed using (API v1)."""

        self.client.get('/api/report/course-feed/rss')

    @task
    def show_feed_v2(self):
        """Simulate the retrieval of the course feed (API v2)."""

        self.client.get('/api/v2/report/course-feed/rss')

    @task
    def show_feed_v2_inst(self):
        """Simulate the retrieval of the course feed for a specific institution (API v2)."""

        self.client.get('/api/v2/report/course-feed/rss/mitx')