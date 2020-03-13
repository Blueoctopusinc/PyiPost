import requests

import exceptions_


class IpostClient(object):

    def __init__(self, username, password, endpoint, client_token, retries=2, timeout=15):
        if endpoint.lower() not in ("g001", "g001"):
            raise exceptions_.PyiPostError(
                "Your endpoint should be either 'g001' or 'g002', you entered {endpoint}".format(endpoint))

        self.base_url = "https://{endpoint}.enterprise.ipost.com/api/v1/".format(endpoint=endpoint)
        self.timeout = timeout
        try:
            self.make_session()
            self.authenticate(username, password)
            self.base_url = "{base_url}{client_token}/".format(base_url=self.base_url, client_token=client_token)
        except exceptions_.PyiPostAuthenticationError as e:
            raise exceptions_.PyiPostError("Authentication Failed: ")

    def make_session(self):
        self.session = requests.session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('https:/', adapter)

    def make_request(self, url, payload, method="GET", extra_params=None, retry_500=True):
        def get(url, payload):
            return self.session.get(url, params=payload, timeout=self.timeout)

        def post(url, payload, extra_params):
            return self.session.post(url, json=payload, timeout=self.timeout, params=extra_params)

        try:
            if method == "GET":
                response = get(url, payload)
            elif method == "POST":
                response = post(url, payload, extra_params)

            response.raise_for_status()

            return response.json()
        except requests.HTTPError as e:
            raise exceptions_.PyiPostHTTPError(e)

    def authenticate(self, client_id, client_secret):
        url = "{base_url}/login".format(base_url=self.base_url)
        payload = {"client_id": client_id,
                   "client_secret": client_secret}
        try:
            response = self.make_request(url, payload, "POST")
        except exceptions_.PyiPostError as e:
            pass
        token = response["data"]["token"]

        header = {"Accept": "/",
                  "Content-Type": "application/json",
                  "X-Auth-Token": token}

        self.session.headers = header
