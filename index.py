import json
import boto3
from botocore.client import Config
import argparse
import arrow

class EC2SnapshotManager:

    def __init__(self):
        self.ec2 = boto3.resource('ec2', config=Config(region_name="ap-southeast-2"))
        self.now = arrow.utcnow()

    def get_delete_time(self, days=15):
        return self.now.shift(days=-days).datetime

    def list_snapshots(self, filters=[]):
        try:
            self.snaps = list(self.ec2.snapshots.filter(OwnerIds=['self'],Filters=filters))
        except Exception as e:
            print('error: failed to list snapshots')
            print(e)
            self.snaps = []
        return self

    def list_amis(self, filters=[]):
        try:
            self.amis = self.ec2.images.filter(Owners=['self'], Filters=filters)
        except Exception as e:
            print('error: failed to list amis')
            print(e)
            self.amis = []
        return self

    def list_volumes(self, filters=[]):
        try:
            self.volumes = self.ec2.volumes.filter(Filters=filters)
        except Exception as e:
            print('error: failed to list volumes')
            print(e)
            self.volumes = []
        return self

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

    def expired_amis(self, days_old=15):
        self.delete_amis = []
        delete_time = self.get_delete_time(days_old)
        for ami in self.amis:
            creation_data = arrow.get(self.ec2.Image(ami.id).creation_date).datetime
            if creation_data < delete_time:
                self.delete_amis.append(ami)
        print()
        print("---------------------------------------------")
        print(len(self.delete_amis), " expired amis.")
        print("---------------------------------------------")
        print()
        return self

    def unused_volumes(self):
        self.delete_volumes = []
        for volume in self.volumes:
            if volume.state == 'available':
                self.delete_volumes.append(volume)
        print()
        print("---------------------------------------------")
        print(len(self.delete_volumes), " unused volumes.")
        print("---------------------------------------------")
        print()
        return self

    def delete_unused_volumes(self, DryRun=True):
        for volume in self.delete_volumes:
            try:
                volume.delete(DryRun)
                print('success: deleted volume (dryrun=%s) : %s ' % (DryRun, volume.id))
            except Exception as e:
                print('error: failed to delete volume %s: %s' % (volume.id, e))

    def deregister_amis(self, DryRun=True):
        for ami in self.delete_amis:
            try:
                ami.deregister(DryRun)
                print('success: deleted ami (dryrun=%s) : %s ' % (DryRun, ami.id))
            except Exception as e:
                print('error: failed to delete ami %s: %s' % (ami.id, e))

    def delete_snapshots(self, DryRun=True):
        for snap in self.delete_snaps:
            try:
                snap.delete(DryRun)
                print('success: deleted snapshot (dryrun=%s) : %s ' % (DryRun, snap.id))
            except Exception as e:
                print('error: failed to delete snapshot %s: %s' % (snap.id, e))

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

    ec2SnapshotManager = EC2SnapshotManager()
    if TYPE == "snapshot":
        ec2SnapshotManager.list_snapshots(filters=FILTERS).expired_snapshots(days_old=AGE).delete_snapshots(DryRun=DRYRUN)
    elif TYPE == "ami":
        ec2SnapshotManager.list_amis(filters=FILTERS).expired_amis(days_old=AGE).deregister_amis(DryRun=DRYRUN)
    elif TYPE == "volume":
        ec2SnapshotManager.list_volumes(filters=FILTERS).unused_volumes().delete_unused_volumes(DryRun=DRYRUN)
    else:
        print("type is wrong, we only support 'snapshot|ami|volume' for now")
