# from __future__ import print_function
# 
import argparse
# import getpass
# import os
# import traceback
import sys
import pkg_resources
# 
# from colorlog import ColoredFormatter
# 
# from sawtooth.gfc_client.client import Client
# from sawtooth.exceptions import Exception
from map_blockchain.addresser import DISTRIBUTION_NAME


def add_create_video_licence_contract_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'create_video_licence_contract',
        help='create_video_licence_contract',
        description='Sends a transaction to create a base asset with the '
        'identifier <name_id>. This transaction will fail if the specified '
        'base asset already exists.',
        parents=[parent_parser])

    parser.add_argument(
        'licenceId',
        type=str,
        help='unique identifier for the asset')
    
    parser.add_argument(
        'videoId',
        type=str,
        help='assetType')
    
    parser.add_argument(
        'licenceOwner',
        type=str,
        help='assetType')

    parser.add_argument(
        'region',
        type=str,
        help='assetType')
    
    parser.add_argument(
        'date_from',
        type=str,
        help='assetType')
    
    parser.add_argument(
        'date_until',
        type=str,
        help='assetType')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--username',
        type=str,
        help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--auth-user',
        type=str,
        help='specify username for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--auth-password',
        type=str,
        help='specify password for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--disable-client-validation',
        action='store_true',
        default=False,
        help='disable client validation')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for game to commit')
    
#====================================================================================

    
#--------------------------------------------------------------------------------------------------

def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='enable more verbose output')

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='display version information')

    return parent_parser

#===============================================================================================================


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands to use the message board by sending message_board transactions.',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    add_create_video_licence_contract_parser(subparsers, parent_parser)
    return parser
