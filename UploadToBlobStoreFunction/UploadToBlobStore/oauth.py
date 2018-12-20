"""
Module with functions to help perform AAD auth
"""
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import datetime
import threading
import json
import adal


from azure.storage.common import TokenCredential

class AutoUpdatedTokenCredential(TokenCredential):
    """
    This class can be used as a TokenCredential.
    It periodically updates its token through a timer triggered operation.
    It shows one way of making sure the credential does not become expired.
    """
    def __init__(self):
        super(AutoUpdatedTokenCredential, self).__init__()

        # a timer is used to trigger a callback to update the token
        # the timer needs to be protected,
        # as later on it is possible that one thread is setting a new timer and
        # another thread is trying to cancel the timer
        self.lock = threading.Lock()
        self.timer_stopped = False

        # get the initial token and schedule the timer for the very first time
        self.refresh_token()

    # support context manager
    def __enter__(self):
        return self

    # support context manager
    def __exit__(self, *args):
        self.stop_refreshing_token()

    def refresh_token(self):
        """
        Function to the get token function to get a new token,
        as well as the time to wait before calling it again
        """
        token, next_interval = self.get_token_func()

        # the token is set instantaneously, and can be used by BlockBlobService right away
        self.token = token

        with self.lock:
            if self.timer_stopped is False:
                self.timer = threading.Timer(next_interval, self.refresh_token)
                self.timer.start()

    def stop_refreshing_token(self):
        """
        The timer needs to be canceled if the application is terminating,
        if not the timer will keep going.
        """
        with self.lock:
            self.timer_stopped = True
            self.timer.cancel()

    @staticmethod
    def get_token_func():
        """
        This function makes a call to AAD to fetch an OAuth token
        :return: the OAuth token and the interval to wait before refreshing it
        """
        print("{}: token updater was triggered".format(datetime.datetime.now()))


        # Get the AAD App ID, secret and tenant ID from disk
        # To test with - with open("aadsettings.dat") as json_data:
        with open('/spn') as json_data:
            aad_settings = json.load(json_data)

        aad_tenant_id = aad_settings["tenantId"]
        aad_client_id = aad_settings["aadClientId"]
        aad_client_secret = aad_settings["aadClientSecret"]

        # in this example, the OAuth token is obtained using the ADAL library
        # however, the user can use any preferred method
        context = adal.AuthenticationContext(
            str.format("https://login.microsoftonline.com/{}", aad_tenant_id),
            api_version=None, validate_authority=True)

        oauth_token = context.acquire_token_with_client_credentials(
            "https://storage.azure.com",
            aad_client_id,
            aad_client_secret)

        # return the token itself and the interval to wait
        # before this function should be called again
        # generally oauth_token['expiresIn'] - 180 is a good interval to give,
        # as it tells the caller to refresh the token 3 minutes before it expires,
        # so here we are assuming that the token expiration
        # is at least longer than 3 minutes, the user should adjust it
        # according to their AAD policy
        return oauth_token['accessToken'], oauth_token['expiresIn'] - 180
