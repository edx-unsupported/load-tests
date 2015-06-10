import os

from locust import HttpLocust

from rss import RSSTasks
from courses import CourseTasks
from instructors import InstructorTasks
from search import SearchTasks
from static import StaticTasks
from marketing import MarketingTasks


class MarketingTest(MarketingTasks):

    tasks = {
        RSSTasks : 10,
        CourseTasks : 40,
        InstructorTasks : 1,
        SearchTasks : 2,
        StaticTasks : 20
    };


class MarketingLocust(HttpLocust):

    # Gets the task set environment variable from the command line
    # If it is not set, the MarketingTest default is used
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'MarketingTest')]
    min_wait = 3 * 1000
    max_wait = 5 * 1000