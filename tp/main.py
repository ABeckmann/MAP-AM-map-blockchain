import sys
import argparse
import pkg_resources

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.log import init_console_logging

from map_blockchain.tp.handler import MapTransactionHandler
from map_blockchain import addresser


def parse_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
 
    parser.add_argument(
        '-C', '--connect',
        help='Endpoint for the validator connection')
 
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='Increase output sent to stderr')
 
    try:
        version = pkg_resources.get_distribution(addresser.DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'
 
    parser.add_argument(
        '-V', '--version',
        action='version',
        version=(addresser.DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='print version information')
 
    return parser.parse_args(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    opts = parse_args(args)
    processor = None
    try:

        processor = TransactionProcessor(url="tcp://localhost:4004")
        init_console_logging(verbose_level=opts.verbose)

        handler = MapTransactionHandler()

        processor.add_handler(handler)
        print("starting tp")
        processor.start()
    except KeyboardInterrupt:
        pass
    except Exception as e:  # pylint: disable=broad-except
        print("Error: {}".format(e))
    finally:
        if processor is not None:
            print("processor is not None: stopping")
            processor.stop()
            
if __name__ == "__main__":
        main()
