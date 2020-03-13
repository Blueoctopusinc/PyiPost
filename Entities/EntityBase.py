class EntityBase(object):
    def __init__(self, client):
        self.client = client

    def build_url(self, action_url):
        return "{base_url}{base_url_path}/{action_url}/".format(base_url=self.client.base_url, base_url_path=self.base_url_path, action_url=action_url)

