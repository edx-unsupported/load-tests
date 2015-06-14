import json
import os
from locust import task, TaskSet


BASIC_AUTH_CREDENTIALS = None
if 'BASIC_AUTH_USER' in os.environ and 'BASIC_AUTH_PASSWORD' in os.environ:
    BASIC_AUTH_CREDENTIALS = (
        os.environ['BASIC_AUTH_USER'],
        os.environ['BASIC_AUTH_PASSWORD']
    )


class AutoAuthTasks(TaskSet):
    """
    Methods useful to any/all tests that want to use auto auth.
    """

    def __init__(self, *args, **kwargs):
        """
        Add basic auth credentials to our client object when specified.
        """
        super(AutoAuthTasks, self).__init__(*args, **kwargs)
        if BASIC_AUTH_CREDENTIALS:
            self.client.auth = BASIC_AUTH_CREDENTIALS

        self._user_id = None
        self._anonymous_user_id = None
        self._username = None
        self._email = None
        self._password = None

    def auto_auth(self, verify_ssl=True, course_id=None):
        """
        Logs in with a new, programmatically-generated user account.
        Requires AUTO_AUTH functionality to be enabled in the target edx instance.

        If `course_id` is specified, enrolls user in course.
        """
        if "sessionid" in self.client.cookies:
            del self.client.cookies["sessionid"]

        params = dict()

        if course_id is not None:
            params['course_id'] = course_id

        response = self.client.get(
            "/auto_auth",
            name="auto_auth",
            params=params,
            headers={'accept': 'application/json'},
            verify=verify_ssl
        )
        json_response = json.loads(response.text)
        self._username = json_response['username']
        self._email = json_response['email']
        self._password = json_response['password']
        self._user_id = json_response['user_id']
        self._anonymous_user_id = json_response['anonymous_id']

    @task
    def stop(self):
        """
        Supports usage as nested or top-level task set.
        """
        if self.parent != self.locust:
            self.interrupt()
