"""
Load test for the Team API.

Usage:

  $ locust --host="http://localhost:8000"

Supported Environment Variables:

  BASIC_AUTH_USER, BASIC_AUTH_PASS - if set, will use for HTTP Authentication
  LOCUST_TASK_SET - if set, will run the specified TaskSet (must be imported in this module)
  LOCUST_MIN_WAIT, LOCUST_MAX_WAIT - use to override defaults set in this module
  COURSE_ID - course that will be tested on the target host, default is set in lms.LmsTasks
  STUDIO_HOST - the URL where Studio is running, default set to http://localhost:8001.

"""
from locust import task, HttpLocust
import os
import sys

# Workaround for Locust running locustfiles as scripts instead of real
# packages.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'team_api'))
from team_api import BaseTeamsTask


class TeamAPITasks(BaseTeamsTask):
    """ Exercise Teams API endpoints. """

    @task(10)
    def create_team(self):
        self._create_team()

    @task(1)
    def update_team(self):
        self._update_team()

    @task(120)
    def list_teams(self):
        self._list_teams()

    @task(40)
    def list_teams_for_topic(self):
        self._list_teams_for_topic()

    @task(50)
    def search_teams(self):
        self._search_teams()

    @task(50)
    def search_teams_for_topic(self):
        self._search_teams_for_topic()

    @task(200)
    def team_detail(self):
        self._team_detail()

    @task(40)
    def list_topics(self):
        self._list_topics()

    @task(120)
    def topic_detail(self):
        self._topic_detail()

    @task(40)
    def list_memberships_for_user(self):
        self._list_memberships_for_user()

    @task(40)
    def list_memberships_for_team(self):
        self._list_memberships_for_team()

    @task(40)
    def change_membership(self):
        self._change_membership()

    @task(5)
    def delete_membership(self):
        self._delete_membership()

    @task(1)
    def stop(self):
        self._stop()


class TeamLocust(HttpLocust):
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'TeamAPITasks')]

    """
    Wait times were chosen using this formula to find an average, then +/- 20%
    desired requests per sec = (number of users) * 1000 / (average wait in ms)

    The assumed values are 15 rps = 100 * 1000 / 6667.
    If more or less than 100 users are desired, scale the wait time by the same
    factor to hold the rps steady, or choose a different factor if changing rps

    These numbers were chosen to be roughly double the daytime throughput of
    Forums (450 rpm = 7.5 rps), as reported on New Relic for prod-edx-forum.
    """

    min_wait = int(os.getenv('LOCUST_MIN_WAIT', 5333))
    max_wait = int(os.getenv('LOCUST_MAX_WAIT', 8000))
