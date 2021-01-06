# import requests
# from bc_python_sawtooth_assets.client.client import Client
# from bc_python_sawtooth_assets.client import cli

import addresser
# from sawtooth_sdk.processor.exceptions import InternalError
REST_API_URL = 'http://localhost:8008'


class Map_video_licence_contract:
    def __init__(self, id, video, licenceOwner, region, date_from, date_until):
        self.id = id
        self.video = video
        self.licenceOwner = licenceOwner
        self.region = region
        self.date_from = date_from
        self.date_until = date_until


# ===============================================================================================

class State(object):
    def __init__(self, context):
        self._context = context    
# ===============================================================================================

    def set_state_video_licence_contract(self, id, video, licenceOwner, region, date_from, date_until):
        """Creates a new map contract
        Args:
            public_key (str): The public key of the user creating the message
            name (str): Unique ID of the message
        """
        address = addresser.make_address_video_licence_contract(id)
        updated_state = self._serialize_video_licence_contract(id, video, licenceOwner, region, date_from, date_until)

        print('adding to BC')
        self._context.set_state({address: updated_state})
        print('worked')

    def _serialize_video_licence_contract(self, id, video, licenceOwner, region, date_from, date_until):
        """Takes a dict of game objects and serializes them into bytes.
        Args:
            games (dict): game name (str) keys, Game values.
        Returns:
            (bytes): The UTF-8 encoded string stored in state.
        """
        print('doing serialize')
        state_str = ",".join([id, video, licenceOwner, region, date_from, date_until])
        print('worked')
        return state_str.encode()

    def isalready_state_video_licence_contract(self, id):
        """gets the data in state
        Args:
            name (str): Unique ID of the message
        """

        address = addresser.make_address_video_licence_contract(id)
        state_data = self._context.get_state([address])
        
        if state_data:
            return True
        else:
            print('no state data- returning None')
            return False

    # def _deserialize_video_licence_contract(self, data):
    #     """Take bytes stored in state and deserialize them into Python
    #     Game objects.
    #     Args:
    #         data (bytes): The UTF-8 encoded string stored in state.
    #     Returns:
    #         (dict): game name (str) keys, Game values.
    #     """
    #     try:
    #         print('decoding data')        
    #         serialized_state = data.decode()
    #         print('worked')
    #         print('deserialize data by splitting') 
    #         name_id, owner, blueprint, cps_device = serialized_state.split(",")
    #         print('worked')
    #         asset = Asset(name_id, owner, blueprint, cps_device)
    #     except ValueError:
    #         raise InternalError("Failed to deserialize game data")
 
    #     return asset
    
    


# ===============================================================================================

