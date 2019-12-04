import json
import boto3
from botocore.client import Config
import argparse
from src.snapshots import Snapshots
from src.volumes import Volumes
from src.amis import Amis

# Below is the main harness
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='deletes ebs snapshots')
    parser.add_argument('-dryrun', help='prints the snapshots to be deleted without deleting them', default='true', action='store', dest='dryrun')
    parser.add_argument('-age', help='specifiy minimum age of snapshots in days to be eligible for deletion', default=365, action='store', dest='age')
    parser.add_argument('-type', help='delete type, only support "snapshot|ami|volume"', default='snapshot', action='store', dest='type')
    parser.add_argument('-filters', help='snapshot filter in json', default=[], type=json.loads)

    args = parser.parse_args()
    AGE = int(args.age)
    TYPE = args.type.lower()
    FILTERS = args.filters
    DRYRUN = args.dryrun.lower() != 'false'

    # ec2SnapshotManager = EC2SnapshotManager()
    if TYPE == "snapshot":
        snapshotCleaner = Snapshots()
        snapshotCleaner.list(Filters=FILTERS).expired(days_old=AGE).delete(DryRun=DRYRUN)
    elif TYPE == "ami":
        amiCleaner = Amis()
        amiCleaner.list(Filters=FILTERS).expired(days_old=AGE).delete(DryRun=DRYRUN)
    elif TYPE == "volume":
        volumeCleaner = Volumes()
        volumeCleaner.list(Filters=FILTERS).unused().delete(DryRun=DRYRUN)
    else:
        print("type is wrong, we only support 'snapshot|ami|volume' for now")
