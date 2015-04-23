"""Locust tests related to basket operations."""
import json

from locust import task

import config
from ecommerce import EcommerceTasks


class BasketsTasks(EcommerceTasks):
    """Contains tasks which exercise basket-related behavior."""

    @task
    def purchase_single_free_product(self):
        """Simulate the purchase of a single free product via the LMS."""
        # If a user tries to purchase the same product more than once, we'll get 409s from
        # the LMS. To avoid this situation, we create a new user each time this task is called.
        self.auto_auth()

        post_data = {
            'course_id': config.COURSE_ID,
        }
        self.post('/commerce/baskets/', data=json.dumps(post_data), name='purchase_single_free_product')
