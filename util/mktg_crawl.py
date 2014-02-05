
import random
import mechanize
import csv

class Crawler(object):
    MAX_DEPTH = 6
    ROOT = 'https://edx-loadtest.elasticbeanstalk.com'
    USER = None
    PASSWORD = None
    EXCLUDE = []


    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        if self.USER and self.PASSWORD:
            self.browser.add_password(self.ROOT, self.USER, self.PASSWORD)
        self.visited = set()

    def crawl(self, start_page):
        print "start page: %s" % (self.ROOT + start_page)

        self.browser.open(self.ROOT + start_page)
        self._crawl_all_links()

    def _crawl_all_links(self, depth=0):

        if depth < self.MAX_DEPTH:

            # Try to get links
            # If we can't (e.g. we're viewing an image)
            # then give up
            try:
                link_list = [link for link in self.browser.links()]
            except:
                return

            for link in link_list:
                if self._should_follow(link):
                    self.visited.add(link.url)
                    print "Following %s" % link.url

                    try:
                        self.browser.follow_link(link)
                    except:
                        print "Could not follow link: {}".format(link)
                        pass
                    else:
                        self._crawl_all_links(depth + 1)

                        # This could fail if, for example the previous link
                        # failed with a redirect loop.
                        try:
                            self.browser.back()
                        except:
                            print "Could not return to previous URL"
                            pass
        else:
            pass

    def _should_follow(self, link):
        # Already been there.
        if link.url in self.visited:
            return False

        # Don't go to another domain.
        if not link.absolute_url.startswith(self.ROOT):
            return False

        # Don't go to "/" because it will effectively shorten the depth.
        # if traversed from the first page.
        if link.url == '/':
            return False

        # Don't go to "#foo" because it will effectively shorten the depth.
        if link.url.startswith('#'.format(self.ROOT)):
            return False

        # Each course has 2 links to it in the course listing pages,
        # one that starts with https://...
        # and the other that starts with /course/...
        # Only follow the second style.
        if link.url.startswith('{}/course/'.format(self.ROOT)):
            return False

        # Specifically do not want to go there.
        if link.url in self.EXCLUDE:
            return False

        return True


if __name__ == '__main__':

    all_links = set()

    crawler = Crawler()
    crawler.crawl('/')

    print "Outputing links..."
    filename = 'marketing_urls.csv'
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        # Randomly shuffle links
        all_link_list = list(crawler.visited)
        random.shuffle(all_link_list)

        for l in all_link_list:
            csv_writer.writerow([l])