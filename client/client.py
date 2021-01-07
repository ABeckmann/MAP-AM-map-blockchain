# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
 

import hashlib
import base64
from base64 import b64encode
import time
import requests
import yaml

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

from map_blockchain.exceptions import Exception
from map_blockchain import addresser


def _sha512(data):
    return hashlib.sha512(data).hexdigest()


class Client:
    def __init__(self, base_url, keyfile=None):

        self._base_url = base_url

        if keyfile is None:
            self._signer = None
            return

        try:
            with open(keyfile) as fd:
                private_key_str = fd.read().strip()
        except OSError as err:
            raise Exception(
                'Failed to read private key {}: {}'.format(
                    keyfile, str(err)))

        try:
            private_key = Secp256k1PrivateKey.from_hex(private_key_str)
        except ParseError as e:
            raise Exception(
                'Unable to load private key: {}'.format(str(e)))
        self._signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_key)
    
    def _send_txn(self,
#                   name_id='',
#                   _id='',
#                   action='',
#                   addresses=[""],
#                   value='',
#                   signed_value='',
#                   remove_signed_value='',
#                   message_text='',
#                   new_owner='',
#                   handle_pk='', 
#                   fork_head_pk='', 
#                   id_plate_pk='',
#                   handle_id='', 
#                   fork_head_id='', 
#                   id_plate_id='',
#                   retainer_thread_batch="", 
#                   retainer_washer_batch="",
#                   retainer_nut_batch="",
#                   screw1_batch="",
#                   screw2_batch="",
#                   usage="", 
#                   repairs="",
#                   security_tag_public_key='',
                  action='',
                  licenceId='',
                  videoId='',
                  licenceOwner='',
                  region='',
                  date_from='',
                  date_until='',
                  addresses=[""],
                  wait=None,
                  auth_user=None,
                  auth_password=None):
        # Serialization is just a delimited utf-8 encoded string
        payload = ",".join([action, licenceId, videoId, licenceOwner, region, date_from,
                date_until]).encode()

        print(f'encodedPayload:{payload}\n')
        print(f'payloadSha512:{_sha512(payload)}\n')
        print(f'addresses:{addresses}\n')

        header = TransactionHeader(
            signer_public_key=self._signer.get_public_key().as_hex(),
            family_name=addresser.FAMILY_NAME,
            family_version=addresser.FAMILY_VERSION,
            inputs=addresses,
            outputs=addresses,
            dependencies=[],
            payload_sha512=_sha512(payload),
            batcher_public_key=self._signer.get_public_key().as_hex(),
            # nonce=time.time().hex().encode()
        ).SerializeToString()
        
        
        print(f'header:{header}\n')
        #print(f'hash(header):{_sha512(header)}\n')

        signature = self._signer.sign(header)

        transaction = Transaction(
            header=header,
            payload=payload,
            header_signature=signature
        )

        print(f'transaction:{transaction}\n')
        #print(f'hash(transaction):{_sha512(transaction)}\n')
        # def _create_batch_list(self, transactions):
        # transaction_signatures = [t.header_signature for t in transactions]

        # header = BatchHeader(
        #     signer_public_key=self._signer.get_public_key().as_hex(),
        #     transaction_ids=transaction_signatures
        # ).SerializeToString()

        # signature = self._signer.sign(header)

        # batch = Batch(
        #     header=header,
        #     transactions=transactions,
        #     header_signature=signature)
        # return BatchList(batches=[batch])

        batch_list = self._create_batch_list([transaction])

        print(f'batch_list:{batch_list}\n')
        print(f'batch_list(encoded):{batch_list.SerializeToString()}\n')
        print(f'generates a list of codes from the characters of bytes')
        print(f'list(batch_list(encoded)):{list(batch_list.SerializeToString())}\n')
        
        
        print(f'hash(batch_list):{_sha512(batch_list.SerializeToString())}\n')
        batch_id = batch_list.batches[0].header_signature
        newFileBytes = batch_list.SerializeToString()
        # make file
        newFile = open(f"{batch_id}.batches", "wb")
        # write to file
        newFile.write(newFileBytes)
        # if wait and wait > 0:
        #     wait_time = 0
        #     start_time = time.time()
        #     response = self._send_request(
        #         "batches", batch_list.SerializeToString(),
        #         'application/octet-stream',
        #         auth_user=auth_user,
        #         auth_password=auth_password)
        #     while wait_time < wait:
        #         status = self._get_status(
        #             batch_id,
        #             wait - int(wait_time),
        #             auth_user=auth_user,
        #             auth_password=auth_password)
        #         wait_time = time.time() - start_time

        #         if status != 'PENDING':
        #             return response

        #     return response

        # return self._send_request(
        #     "batches", batch_list.SerializeToString(),
        #     'application/octet-stream',
        #     auth_user=auth_user,
        #     auth_password=auth_password)
    
    def create_video_licence_contract(self, licenceId, videoId, licenceOwner, region, date_from,
                date_until, wait=None, auth_user=None, auth_password=None):
        return self._send_txn( 
            action="create_video_licence_contract",
            licenceId=licenceId,
            videoId=videoId,
            licenceOwner=licenceOwner,
            region=region,
            date_from=date_from,
            date_until=date_until,
            wait=wait,
            auth_user=auth_user,
            auth_password=auth_password)
    
    def list_msg(self, auth_user=None, auth_password=None):
        list(type=addresser.MESSAGE, auth_user=auth_user, auth_password=auth_password)
 
    def list_gfc_fork(self, auth_user=None, auth_password=None):
        list(type=addresser.GFC_FORK, auth_user=auth_user, auth_password=auth_password)

    def list(self, _type, auth_user=None, auth_password=None):
    
        prefix = addresser.NAMESPACE + _type

        result = self._send_request(
            "state?address={}".format(prefix),
            auth_user=auth_user,
            auth_password=auth_password)

        try:
            encoded_entries = yaml.safe_load(result)["data"]

            return [
                base64.b64decode(entry["data"]) for entry in encoded_entries
            ]

        except BaseException:
            return None

    def get_addresses_of_children(self, parent, auth_user=None, auth_password=None):
        print('get_addresses_of_children')
        print('address of parent = {}'.format(addresser._make_address_assembly_map_parent(parent)))
        print('address of parent + child = {}'.format(addresser._make_address_assembly_map(parent, 
            '1111013a941a4b495a929f0ce35cb8b780b3c74734aafdddccaaf3b05923a8608f')))

        _rest_api = "state?address={}".format(addresser._make_address_assembly_map_parent(parent))
        print('getting result from send request with format: {}'.format(_rest_api))
        result = self._send_request(
            _rest_api, # NOTE this can only be a maximum of 12 hex long!!
            auth_user=auth_user,
            auth_password=auth_password)
        print('success: getting result from send request with format: {}'.format(_rest_api))
        
        data_with_first_12_hex_matching_parent = self._yaml_load_data(result)
        print('loading the data: {}'.format(data_with_first_12_hex_matching_parent))
        
        obj_list = [
        obj.split(',')
        for objs in data_with_first_12_hex_matching_parent
        for obj in objs.decode().split('|')
        ]
        asset_maps_of_parents_list = []
        parent_hash = addresser._hash(parent, 31)
        for addresses in obj_list:
            if addresses[0][8:39] == parent_hash:
                print('true- addresses[0][8:39]: {}\n parent: {}'.format(addresses[0][8:39], parent_hash))
                asset_maps_of_parents_list.append(addresses[0])
            else:
                print('false- addresses[0][8:39]: {}\n parent: {}'.format(addresses[0][8:39], parent_hash))
        
        print('asset_maps_of_parents_list: \n{}'.format(asset_maps_of_parents_list))
        return asset_maps_of_parents_list
        #print('\n printing obj_list \n{}'.format(obj_list))
        
    def _yaml_load_data(self, result):
        try:
            encoded_entries = yaml.safe_load(result)["data"]

            return [
#                 [base64.b64decode(entry['address']), base64.b64decode(entry['data'])] for entry in encoded_entries
                base64.b64decode(entry["data"]) for entry in encoded_entries

            ]

        except BaseException:
            return None
        
        #TODO make sure its not a 404 error/ if statement that says there are no children in that case
        
    def show(self, name, address, auth_user=None, auth_password=None):
        print('doing show')
        result = self._send_request(
            "state/{}".format(address),
            name=name,
            auth_user=auth_user,
            auth_password=auth_password)
        print('SUCCESS: doing show')
        try:
            print('Returning show data')
            return base64.b64decode(yaml.safe_load(result)["data"])
 
        except BaseException:
            return None
        
    def history(self, name, address, auth_user=None, auth_password=None):
        print('doing history')
        #TODO using this method will only show one block to another bocks' history. 
        #This will skip history within a block. (e.g. in a block remove & add component = history not showing part removed only that the 
        # new part is now there)
        
        _blocks = self._send_request(
            "blocks?", # ./{}".format(address)
            name=name,
            auth_user=auth_user,
            auth_password=auth_password)
        
#         if _blocks is not None:

#             block_list = []
#             
#             for block in _blocks.split()
            
            
#             owner, msg = {
#                 name: (owner, msg)
#                 for name, owner, msg in [
#                     hw.split(',')
#                     for hw in data.decode().split('|')
#                     ]
#                 }[name]
        
        #_batches, _header, _header_signature _blocks
        
#         result = self._send_request(
#             "state/{}".format(address),
#             name=name,
#             auth_user=auth_user,
#             auth_password=auth_password)
#         print('SUCCESS: doing show')
        try:
            print('Returning history data')
            return yaml.safe_load(_blocks)['data']
 
        except BaseException:
            return None

    def _get_status(self, batch_id, wait, auth_user=None, auth_password=None):
        try:
            result = self._send_request(
                'batch_statuses?id={}&wait={}'.format(batch_id, wait),
                auth_user=auth_user,
                auth_password=auth_password)
            return yaml.safe_load(result)['data'][0]['status']
        except BaseException as err:
            raise Exception(err)
# response = self._send_request(
#                 "batches", batch_list.SerializeToString(),
#                 'application/octet-stream',
#                 auth_user=auth_user,
#                 auth_password=auth_password)

    def _send_request(self,
                      suffix,
                      data=None,
                      content_type=None,
                      name=None,
                      auth_user=None,
                      auth_password=None):
        if self._base_url.startswith("http://"):
            url = "{}/{}".format(self._base_url, suffix)
        else:
            url = "http://{}/{}".format(self._base_url, suffix)

        print(f'suffix:{suffix}')
        print(f'data:{data}\n')
        headers = {}
        if auth_user is not None:
            auth_string = "{}:{}".format(auth_user, auth_password)
            b64_string = b64encode(auth_string.encode()).decode()
            auth_header = 'Basic {}'.format(b64_string)
            headers['Authorization'] = auth_header

        if content_type is not None:
            headers['Content-Type'] = content_type

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if result.status_code == 404:
                raise Exception("No such message: {}".format(name))

            elif not result.ok:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise Exception(
                'Failed to connect to {}: {}'.format(url, str(err)))

        except BaseException as err:
            raise Exception(err)

        return result.text

    def _create_batch_list(self, transactions):
        transaction_signatures = [t.header_signature for t in transactions]

        header = BatchHeader(
            signer_public_key=self._signer.get_public_key().as_hex(),
            transaction_ids=transaction_signatures
        ).SerializeToString()

        signature = self._signer.sign(header)

        batch = Batch(
            header=header,
            transactions=transactions,
            header_signature=signature)
        return BatchList(batches=[batch])
