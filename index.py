import os
import sys
import json
sys.path.append("{}/lib".format(os.getcwd()))
import boto3
import argparse
from datetime import datetime, timedelta

DRYRUN = bool(os.environ.get('CLNR_EBS_SNAP_DRYRUN', 1))
AGE = int(os.environ.get('CLNR_EBS_SNAP_AGE', 365))
FILTER = json.loads(os.environ.get('CLNR_EBS_SNAP_FILTER', '[]'))

def handler(event, context):
    try:
      ec2 = boto3.resource('ec2')
    except Exception as e:
        print('error: failed to initialize boto3 client')
        print(e)
        sys.exit(1)

    print('ebs snapshot age set to: %s' % (AGE))
    print('snapshot filter set to: %s' % (FILTER))
    snaps = list_snapshots(ec2)
    now = datetime.utcnow()
    candidates = expired_snapshots(snaps,now,AGE)
    print('number of snaps for deletion: {0:d}'.format(len(candidates)))
    delete_snapshots(ec2,candidates)

def list_snapshots(ec2):
    try:
        snaps = list(ec2.snapshots.filter(OwnerIds=['self'],Filters=FILTER))
    except Exception as e:
        print('error: failed to list snapshots')
        print(e)
        return []
    return snaps

def expired_snapshots(snaps,now=datetime.utcnow(),days_old=AGE):
    delete_snaps = []
    delete_time = get_delete_time(now,days_old)
    for snap in snaps:
        if snap.start_time < delete_time:
            delete_snaps.append(snap)
            print('expired snapshot: %s, %s' % (snap.id, snap.start_time))
    return delete_snaps

def delete_snapshots(ec2,snaps):
    try:
        for snap in snaps:
            snap.delete(DryRun=DRYRUN)
    except Exception as e:
        print('error: failed to delete snapshot %s: %s' % (snap.id, e))

def get_delete_time(now=datetime.utcnow(),days_old=AGE):
    thisTz = now.astimezone().tzinfo
    delete_time = now - timedelta(days=days_old)
    # need to add a timezone to the timedelta to allow comparision with snap start time
    return delete_time.replace(tzinfo=thisTz)

# Below is the main harness
if __name__ == '__main__':
    request = {"None": "None"}
    parser = argparse.ArgumentParser(description='deletes ebs snapshots')
    parser.add_argument('-dryrun', help='prints the snapshots to be deleted without deleting them', default='true', action='store', dest='dryrun')
    parser.add_argument('-age', help='specifiy minimum age of snapshots in days to be eligible for deletion', default=365, action='store', dest='age')
    parser.add_argument('-filters', help='snapshot filter in json', default=[], type=json.loads)

    args = parser.parse_args()
    DRYRUN = args.dryrun.lower() != 'false'
    AGE = int(args.age)
    FILTER = args.filters
    handler(request, None)
