import arrow
from src.ec2 import EC2

class Snapshots(EC2):

    def list(self, Filters=[]):
        try:
            self.snaps = list(self.ec2.snapshots.filter(OwnerIds=['self'],Filters=Filters))
        except Exception as e:
            print('error: failed to list snapshots')
            print(e)
            self.snaps = []
        return self

    def expired(self, days_old=15):
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

    def delete(self, DryRun=True):
        for snap in self.delete_snaps:
            try:
                snap.delete(DryRun)
                print('success: deleted snapshot (dryrun=%s) : %s ' % (DryRun, snap.id))
            except Exception as e:
                print('error: failed to delete snapshot %s: %s' % (snap.id, e))
