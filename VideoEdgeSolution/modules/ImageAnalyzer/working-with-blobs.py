import sys
import logging
import argparse
from azure.storage.blob import BlobType, BlobServiceClient

azureLogger = logging.getLogger('azure')
azureLogger.setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

# cloud storage
cloudAccountUrl = ""
cloudAccountKey = ""

# local storage
localAccountUrl = "http://127.0.0.1:11002/<storage-account-name>"
localAccountKey = ""

try:
    # capture script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--container', type=str, dest='container', help="Container name.")
    parser.add_argument('--blob', type=str, dest='blob', help="Blob name, including virtual subfolder path.")
    parser.add_argument('--text', type=str, dest='text', help="Text to write/append to blob.")
    parser.add_argument('--action', type=str, dest='action', default='w', help="Action to perform. Use 'w' to write and 'a' to append.")
    parser.add_argument('--local', type=bool, dest='local', default=False, help="Whether to connect to local storage account. Default is False.")
    args = parser.parse_args()

    if args.local:
        blob_service_client = BlobServiceClient(localAccountUrl, localAccountKey)
    else:
        blob_service_client = BlobServiceClient(cloudAccountUrl, cloudAccountKey)

    logger.info("Connected to account '%s'" % blob_service_client.account_name)

    try:
        blob_service_client.create_container(args.container)
        logger.info("created container '%s'" % args.container)
    except Exception as e:
        logger.info("container '%s' already exists" % args.container)

    blob_client = blob_service_client.get_blob_client(container=args.container, blob=args.blob)

    # write operation is the same for both cloud and local storage
    if args.action == 'w':
        logger.info("Writing to '%s/%s'" % (args.container, args.blob))
        blob_client.upload_blob(args.text, blob_type=BlobType.BlockBlob)
    # append operation
    elif args.action == 'a':
        if not blob_client.exists():
            logger.info("creating append blob '%s/%s'" % (args.container, args.blob))
            blob_client.create_append_blob()
        
        logger.info("Appending to '%s/%s'" % (args.container, args.blob))
        blob_client.append_block(args.text)
 
    logger.info("Operation completed")
except Exception as e:
    logger.exception(e)
