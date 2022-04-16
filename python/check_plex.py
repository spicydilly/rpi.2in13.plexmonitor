"""
This module uses the Tautulli API to gather current stats from Plex
"""
import os
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

class PlexClient ():
    """Class for api requests to Tautulli"""
    BASE_URL = f"https://{os.environ['TAUTULLI_ADDRESS']}/api/v2?apikey="\
        f"{os.environ['TAUTULLI_API_KEY']}&cmd="
    HEADERS = {'Content-type': 'application/json'}

    def get(self, uri):
        """Get request"""
        url = f'{self.BASE_URL}{uri}'
        return requests.get(url, headers=self.HEADERS, verify=False)

def check_if_alive (client):
    """
    Checks if plex is alive

        Returns :
            True - if Plex is alive
            False - if Tautulli or Plex can't be reached, or if error
    """
    check_url = 'server_status'
    check_request = client.get(check_url)
    check_json = check_request.json()
    if check_request.status_code == 200:
        logging.info(check_json)
        if check_json['response']['data']['connected']:
            return True
        return False
    logging.error("Error connecting to tautulli!\nError : %s", check_request.status_code)
    return False

def get_activity (client):
    """
    Checks current activity on Plex

        Returns :
            [Num Streams, Total Bandwidth]
            False - If error
    """
    activity_url = 'get_activity'
    activity_request = client.get(activity_url)
    activity_json = activity_request.json()
    if activity_request.status_code == 200:
        logging.info(activity_json)
        return [ str(activity_json['response']['data']['stream_count']),
            str(activity_json['response']['data']['total_bandwidth']),
            activity_json['response']['data']['sessions'] ]
    logging.error("Error connecting to tautulli!\nError : %s", activity_request.status_code)
    return False

def check_for_update (client):
    """
    Checks for any updates available on Plex

        Returns :
            True - If update available
            False - No update available or if error
    """
    update_url = 'get_pms_update'
    update_request = client.get(update_url)
    update_json = update_request.json()
    if update_request.status_code == 200:
        logging.info(update_json)
        if update_json['response']['data']['update_available']:
            return True
        return False
    logging.error("Error connecting to tautulli!\nError : %s", update_request.status_code)
    return False

if __name__ == '__main__':
    plex_client = PlexClient()
    check_if_alive(plex_client)
    get_activity(plex_client)
    check_for_update(plex_client)
