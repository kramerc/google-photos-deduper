# import google.auth
# import requests
from google.auth.transport.requests import AuthorizedSession
# import pprint
# import json
from google_photos_deduper.media_items.repository import MediaItemsRepository
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import pprint

class Client:
    """A simple class"""

    def __init__(self, session: AuthorizedSession):
        self.__configure_requests_session(session)
        self.session = session

        user_info = self.__get_user_info()
        self.repo = MediaItemsRepository(user_id=user_info['id'])

    def local_media_items_count(self):
        return self.repo.count()

    def gather_media_items(self):
        max_items = 100_000
        next_page_token = None
        item_count = 0
        params = {
            "pageSize": 100
        }
        
        while item_count < max_items:
            if (next_page_token):
                params['pageToken'] = next_page_token

            resp = self.session.get(
                'https://photoslibrary.googleapis.com/v1/mediaItems',
                params=params
            )
            resp_json = resp.json()

            # logging.info(pprint.pformat(resp_json))
            # logging.info(json.dumps(resp_json, indent=4, sort_keys=True))
        
            if 'mediaItems' in resp_json:
                for media_item_json in resp_json['mediaItems']:
                    self.repo.create_if_not_exists(media_item_json)
                
                item_count += len(resp_json['mediaItems'])
            
            next_page_token = resp_json['nextPageToken']
            if not next_page_token:
                break

            logging.info(f'Retrieved {item_count} mediaItems so far')

        logging.info('Done retrieving mediaItems')

        # for media_item in self.repo.all():
        #     logging.info(pprint.pformat(media_item))
    
    def __configure_requests_session(self, session):
        # Automatically raise errors 
        session.hooks = {
            'response': lambda r, *args, **kwargs: r.raise_for_status()
        }

        # Retry up to 3 times on 503 response
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[503]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

    def __get_user_info(self):
        return self.session.get('https://www.googleapis.com/userinfo/v2/me').json()
