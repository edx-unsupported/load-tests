from helpers import CsApiCall
import os
from random import sample


class Transaction(CsApiCall):
    def __init__(self):
        super(Transaction, self).__init__()
        return

    def run(self):
        self.get_user()

        timer_name = "cs_get_comments"
        comment_id = self._get_comment_id()
        method = 'get'
        url = '%s/comments/%s' % (self.service_host, comment_id)
        data_or_params = {
            'api_key': self.api_key,
            'recursive': False
        }
        self.perform_request(
            timer_name=timer_name, method=method,
            url=url, data_or_params=data_or_params
        )

        self.get_user()
        self.delay_for_pacing()
        return

    def _get_comment_id(self):
        # read in a list of possible threads to use
        this_dir = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(this_dir, '../data/comments.txt')
        with open(fname) as f:
            self.comments = f.readlines()

        # choose a random comment
        self.comment_id = sample(self.comments, 1)[0].rstrip('\n')
        return self.comment_id

# define main so that we can test out the script with
# `python <filename>`
if __name__ == '__main__':
    t = Transaction()
    t.run()