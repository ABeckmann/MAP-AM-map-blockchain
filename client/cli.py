from __future__ import print_function

import getpass
import logging
import os
import traceback
import sys

from colorlog import ColoredFormatter

from map_blockchain.client.client import Client
from map_blockchain.exceptions import Exception


from map_blockchain.client.cli_parser import create_parser

#DISTRIBUTION_NAME = addresser.DISTRIBUTION_NAME
DEFAULT_URL = 'http://localhost:8008'


def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)

    if verbose_level == 0:
        clog.setLevel(logging.WARN)
    elif verbose_level == 1:
        clog.setLevel(logging.INFO)
    else:
        clog.setLevel(logging.DEBUG)

    return clog


def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))
    
#===============================================================================================================

#def do_create_base_asset(args):
#    security_tag_public_key = args.security_tag_public_key
#    asset_type = args.asset_type
    
#    url = _get_url(args)
#    keyfile = _get_keyfile(args)
#    auth_user, auth_password = _get_auth_info(args)

#    client = Client(base_url=url, keyfile=keyfile)

#    if args.wait and args.wait > 0:
#        response = client.create_base_asset(
#            security_tag_public_key,
#            asset_type,
#            wait=args.wait,
#            auth_user=auth_user,
#            auth_password=auth_password)
#    else:
#        response = client.create_base_asset(
#            security_tag_public_key, 
#            asset_type,
#            auth_user=auth_user, 
#            auth_password=auth_password)
        

#    print("Response: {}".format(response))
    
#===============================================================================================================


#===============================================================================================================


def do_create_video_licence_contract(args):
    
    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)

    client = Client(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.create_video_licence_contract(
            args.licenceId,
            args.videoId,
            args.licenceOwner,
            args.region,
            args.date_from,
            args.date_until,
            wait=args.wait,
            auth_user=auth_user,
            auth_password=auth_password)
    else:
        response = client.create_video_licence_contract(
            args.licenceId,
            args.videoId,
            args.licenceOwner,
            args.region,
            args.date_from,
            args.date_until,
            auth_user=auth_user, 
            auth_password=auth_password)
    print("Response: {}".format(response))
#===============================================================================================================


#===============================================================================================================

def _get_url(args):
    return DEFAULT_URL if args.url is None else args.url


def _get_keyfile(args):
#     username = getpass.getuser() if args.username is None else args.username
#     home = os.path.expanduser("~")
#     key_dir = os.path.join(home, ".sawtooth", "keys")
#     return '{}\\{}.priv'.format(key_dir, username)
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".keys")
    return '{}\\{}.priv'.format(key_dir, 'bob')
    
    #return '{}\\{}.priv'.format('C:\\Users\\Sawtooth\\git\\gfc\\sawtooth\\keys', 'bob')


def _get_auth_info(args):
    auth_user = args.auth_user
    auth_password = args.auth_password
    if auth_user is not None and auth_password is None:
        auth_password = getpass.getpass(prompt="Auth Password: ")

    return auth_user, auth_password

#===============================================================================================================


def main(prog_name=os.path.basename(sys.argv[0]), args=None):
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(prog_name)
    args = parser.parse_args(args)

    if args.verbose is None:
        verbose_level = 0
    else:
        verbose_level = args.verbose

    setup_loggers(verbose_level=verbose_level)
    print('command: {}'.format(args.command))
    if args.command == 'create_video_licence_contract':
        do_create_video_licence_contract(args)
    # elif args.command == 'update_meter_value':
    #     do_update_meter_value(args)
    # elif args.command == 'create_blueprint':
    #     do_create_blueprint(args)
    # elif args.command == 'add_blueprint_connection_string':
    #     do_add_blueprint_connection_string(args)
    # #elif args.command == 'create_virtual_asset':
    # #    do_create_virtual_asset(args)
    # elif args.command == 'create_cps_device':
    #     do_create_cps_device(args)
    # elif args.command == 'create_assembly_map':
    #     do_create_assembly_map(args)
    # elif args.command == 'remove_assembly_map':
    #     do_remove_assembly_map(args)
        
    else:
        raise Exception("invalid command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except Exception as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException: # as err
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main_wrapper()

# 
# def do_addresser(args):
#     _id = args.id
#     _type = args.type
#     if _type == 'gfc_fork':
#         print(addresser._make_address_gfc_fork(_id))
#     elif _type == 'handle':
#         print(addresser._make_address_handle(_id))
#     elif _type == 'fork_head':
#         print(addresser._make_address_fork_head(_id))
#     elif _type == 'id_plate':
#         print(addresser._make_address_id_plate(_id))

