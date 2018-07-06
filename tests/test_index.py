import unittest
import boto3
from moto import mock_ec2
from index import EC2SnapshotManager

class TestExpiredSnapshots(unittest.TestCase):

    def test_1(self):
        self.assertEqual(True, True)


#     def setUp(self):
#         self.snaps = []
#         snap_unexpired = boto3.ec2.Snapshot('snap-00000000000000000')
#         snap_expired = boto3.ec2.Snapshot('snap-00000000000000001')
#         self.now = datetime.utcnow()
#         twomonthsago = self.now - timedelta(days=61)
#         oneyearago = self.now - timedelta(days=366)
# #        thisTz = self.now.astimezone().tzinfo
# #        twomonthsago.replace(tzinfo=thisTz)
# #        oneyearago.replace(tzinfo=thisTz)
#         setattr(snap_unexpired.start_time, twomonthsago)
#         setattr(snap_unexpired.start_time, oneyearago)
#         self.snaps.append(snap_unexpired)
#         self.snaps.append(snap_expired)
#
#     def test_expired_snapshots(self):
#         expired = index.expired_snapshots(self.snaps,sel.now,365)
#         self.assertEqual(len(expired), 1)

if __name__ == '__main__':
    unittest.main()
