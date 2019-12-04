import arrow
from src.ec2 import EC2

class Volumes(EC2):

    def list(self, Filters=[]):
        try:
            self.volumes = self.ec2.volumes.filter(Filters=Filters)
        except Exception as e:
            print('error: failed to list volumes')
            print(e)
            self.volumes = []
        return self

    def unused(self):
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

    def delete(self, DryRun=True):
        for volume in self.delete_volumes:
            try:
                volume.delete(DryRun)
                print('success: deleted volume (dryrun=%s) : %s ' % (DryRun, volume.id))
            except Exception as e:
                print('error: failed to delete volume %s: %s' % (volume.id, e))
