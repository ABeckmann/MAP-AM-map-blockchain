
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction

import addresser # from map_blockchain 
from .state import State
# from bc_python_sawtooth_assets.tp.state import Asset

# C:\Users\alexa\Source\Repos\alexander-milne\bc_python_sawtooth_assets\bc_python_sawtooth_assets\bc_python_sawtooth_assets\encryption\sawtooth_signing_helper.py
# from secp256k1_signing_helper.encryption.sawtooth_signing_helper import verify_with_pk


class MapTransactionHandler(TransactionHandler):
 
    @property
    def family_name(self):
        return addresser.FAMILY_NAME
    
    @property
    def family_versions(self):
        return [addresser.FAMILY_VERSION]
    
    @property
    def namespaces(self):
        return [addresser.NAMESPACE]
    
    @property
    def namespace(self):
        return addresser.NAMESPACE

    def apply(self, transaction, context):
        print()
        print('          New Transaction')
        # header = transaction.header
        # The transaction signer_public_key is the creator of the transaction
        # signer_public_key = header.signer_public_key
        state = State(context)

        # 1. Deserialize the transaction and verify it is valid
        print('Deserialize the transaction')

        try:
            # The payload is csv utf-8 encoded string
            (action, licenceId, videoId, licenceOwner, region, date_from,
                date_until) = transaction.payload.decode().split(",")
        except ValueError:
            raise InvalidTransaction("Invalid payload serialization")

        print('SUCCESS - Deserialize the transaction')

        print('validate_transaction')
#         _validate_transaction(action, name_id, owner)
        print('SUCCESS - validate_transaction')
        print('action is: {}'.format(action))

#         if action == 'transfer_ownership':
#             if signer_public_key !=  state.get_state_message_board_message(name).owner:
#                 raise InvalidTransaction('Transaction signer_public_key is not the owner of the message')
#
#             print('transfer ownership')   
#             state.set_state_message_board_message(name, new_owner, state.get_state_message_board_message(name).message_text)

# ==============================================================================

        if action == 'create_video_licence_contract':
            # inputs name_id, list_of_blueprint_connections
            print('action: {} id: {}'.format(action, licenceId))
            if state.isalready_state_video_licence_contract(licenceId):
                raise InvalidTransaction(
                    'Invalid action: data already exists: {}'.format(licenceId))

            state.set_state_video_licence_contract(licenceId, videoId, licenceOwner,
                                                region, date_from, date_until)

# ==============================================================================
