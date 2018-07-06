import unittest
import boto3
from botocore.client import Config
from datetime import datetime, timedelta
from moto import mock_ec2
from index import EC2SnapshotManager

@mock_ec2
class TestExpiredSnapshots(unittest.TestCase):

    @mock_ec2
    def setUp(self):
        self.ec2 = boto3.client("ec2", config=Config(region_name="ap-southeast-2"))
        self.volume = self.create_volume()
        self.snap1 = self.create_snapshot(self.volume)
        self.snap2 = self.create_snapshot(self.volume)

    def create_volume(self):
        return self.ec2.create_volume(
            AvailabilityZone='ap-southeast-2a',
            Encrypted=False,
            Iops=123,
            Size=10,
            VolumeType='standard',
            DryRun=False,
            TagSpecifications=[
                {
                    'ResourceType': 'volume',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'TestVolume'
                        },
                    ]
                },
            ]
        )

    def create_snapshot(self, volume_object):
        return self.ec2.create_snapshot(
            Description='TestCreateSanpshots',
            VolumeId=volume_object["VolumeId"],
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'TestSnapshot'
                        },
                    ]
                },
            ],
            DryRun=False
        )


    def delete_volume(self, volume_object):
        self.ec2.delete_volume(
            VolumeId=volume_object["VolumeId"],
            DryRun=False
        )


    def delete_snapshot(self, snapshot_object):
        self.ec2.delete_snapshot(
            SnapshotId=snapshot_object["SnapshotId"],
            DryRun=False
        )

    # def add_days(self, days=10):
    #     now = datetime.utcnow()
    #     thisTz = now.astimezone().tzinfo
    #     new_time = now - timedelta(days)
    #     return new_time.replace(tzinfo=thisTz)

    def test_list_snapshots(self):
        ec2SnapshotManager = EC2SnapshotManager()
        ec2SnapshotManager.list_snapshots(filters=[{"Name": "tag:Name", "Values": ["TestSnapshot"]}])
        self.assertEqual(len(ec2SnapshotManager.snaps), 2)


    def test_expired_snapshots_return_none(self):
        ec2SnapshotManager = EC2SnapshotManager()
        ec2SnapshotManager.list_snapshots(filters=[{"Name": "tag:Name", "Values": ["TestSnapshot"]}]).expired_snapshots(days_old=5)
        self.assertEqual(len(ec2SnapshotManager.delete_snaps), 0)

    def test_expired_snapshots_return_2(self):
        ec2SnapshotManager = EC2SnapshotManager()
        ec2SnapshotManager.list_snapshots(filters=[{"Name": "tag:Name", "Values": ["TestSnapshot"]}]).expired_snapshots(days_old=0)
        self.assertEqual(len(ec2SnapshotManager.delete_snaps), 2)

    @mock_ec2
    def teardown():
        self.delete_volume(self.volume)
        self.delete_snapshot(self.snap1)
        self.delete_snapshot(self.snap2)

if __name__ == '__main__':
    unittest.main()
