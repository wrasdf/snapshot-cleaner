import json
import boto3
from botocore.client import Config
import argparse
from datetime import datetime, timedelta

class EC2SnapshotManager:

    def __init__(self):
        self.ec2 = boto3.resource('ec2', config=Config(region_name="ap-southeast-2"))
        self.now = datetime.utcnow()

    def list_snapshots(self, filters=[]):
        try:
            self.snaps = list(self.ec2.snapshots.filter(OwnerIds=['self'],Filters=filters))
        except Exception as e:
            print('error: failed to list snapshots')
            print(e)
            self.snaps = []
        return self

    def get_delete_time(self, days=15):
        now = self.now
        thisTz = now.astimezone().tzinfo
        delete_time = now - timedelta(days)
        # need to add a timezone to the timedelta to allow comparision with snap start time
        return delete_time.replace(tzinfo=thisTz)

    def expired_snapshots(self, days_old=15):
        self.delete_snaps = []
        delete_time = self.get_delete_time(days_old)
        for snap in self.snaps:
            if snap.start_time < delete_time:
                self.delete_snaps.append(snap)
                # print('expired snapshot: %s, %s' % (snap.id, snap.start_time))
        print()
        print("---------------------------------------------")
        print(len(self.delete_snaps), " expired snapshots.")
        print("---------------------------------------------")
        print()
        return self

    def delete_snapshots(self, DryRun=True):
        for snap in self.delete_snaps:
            try:
                snap.delete(DryRun)
                print('success: deleted snapshot: %s' % (snap.id))
            except Exception as e:
                print('error: failed to delete snapshot %s: %s' % (snap.id, e))

# Below is the main harness
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='deletes ebs snapshots')
    parser.add_argument('-dryrun', help='prints the snapshots to be deleted without deleting them', default='true', action='store', dest='dryrun')
    parser.add_argument('-age', help='specifiy minimum age of snapshots in days to be eligible for deletion', default=365, action='store', dest='age')
    parser.add_argument('-filters', help='snapshot filter in json', default=[], type=json.loads)

    args = parser.parse_args()
    DRYRUN = args.dryrun.lower() != 'false'
    AGE = float(args.age)
    FILTERS = args.filters

    ec2SnapshotManager = EC2SnapshotManager()
    ec2SnapshotManager.list_snapshots(filters=FILTERS).expired_snapshots(days_old=AGE).delete_snapshots(DryRun=DRYRUN)
