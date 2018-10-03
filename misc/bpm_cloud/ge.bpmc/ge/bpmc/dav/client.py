# -*- coding: utf-8 -*-

import requests
import webdav3.client as wc
from webdav3.exceptions import *


class BPMDavClient(wc.Client):

    request_options = {}

    def execute_request(self, action, path, data=None, headers_ext=None):
        """
        A wc.Client execute_request method override to handle
        additional request options (self.request_options) such
        as certificate authority, ...
        Returns a requests.request.response
        """
        response = requests.request(
            method=BPMDavClient.requests[action],
            url=self.get_url(path),
            auth=(self.webdav.login, self.webdav.password),
            headers=self.get_headers(action, headers_ext),
            timeout=self.timeout,
            data=data,
            **self.request_options
        )
        if response.status_code == 507:
            raise NotEnoughSpace()
        if response.status_code >= 400:
            raise ResponseErrorCode(
                url=self.get_url(path),
                code=response.status_code, message=response.content)
        return response
