import requests
import os

class EnginesAuthException(Exception):
    pass

class InvalidResponseException(Exception):
    status_code = None

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class Engines:
    __ACCESS_TOKEN = None
    API_URL = "https://engines.primer.ai/api/v1"

    def __init__(self,access_token, debug=True) -> None:
        self.SESSION = requests.Session()
        self.__ACCESS_TOKEN = access_token
        self.__DEBUG = debug

        self.set_access_token(access_token)

    def __log(self, msg):
        if self.__DEBUG:
            print(msg)

    def __handle_json_response(self, resp):
        """Ensure a valid JSON response

        Args:
            resp: A `requests` Response object

        Raises:
            AutomateAuthException: If a 401 is returned by an endpoint
            InvalidResponseException: If an invalid status code is returned (not a 200 or 201)

        Returns:
            object: the deserialized json
        """
        if resp.status_code == 401:
            raise EnginesAuthException

        if resp.status_code == 204:
            return None

        if (
            resp.status_code != 200
            and resp.status_code != 201
            and resp.status_code != 202
        ):
            raise InvalidResponseException(resp.status_code, resp.text)

        return resp.json()

    def set_access_token(self, access_token):
        self.__ACCESS_TOKEN = access_token
        self.SESSION.headers.update({"Authorization": f"Bearer {self.__ACCESS_TOKEN}"})

    def __handle_request(self, method, url, **kwargs):
        """Helper function to use in most methods

        Args:
            method (str): [description]
            url (str): URL to send the request to
            \*\*kwargs: Optional arguments that ``request`` takes.
        """

        def infunc_request():
            r = self.SESSION.request(method, url, **kwargs)
            resp = self.__handle_json_response(r)
            return resp

        try:
            resp = infunc_request()
        except EnginesAuthException as e:
            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            resp = infunc_request()
        return resp

    def topics_abstractive(self, text):
        """Calls Engines Topics model.

        Args:
            text (str): Input text.

        Returns:
            obj: The response from the Engines Topics model
        """
        request_args = {
            "url": f"{self.API_URL}/generate/abstractive_topics",
            "json": {"text": text},
            "headers": {"content-type": "application/json"},
        }
        resp = self.__handle_request('post',**request_args)
        return resp

    def ner_resolved(self, text):
        """Calls Engines NER model with resolution.

        Args:
            text (str): Input text.

        Returns:
            obj: The response from the Engines NER model
        """
        request_args = {
            "url": f"{self.API_URL}/entities/resolved",
            "json": {"text": text},
            "headers": {"content-type": "application/json"},
        }
        resp = self.__handle_request('post',**request_args)
        return resp
