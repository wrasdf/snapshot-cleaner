import arrow
from src.ec2 import EC2

class Amis(EC2):

    def list(self, Filters=[]):
        try:
            self.amis = self.ec2.images.filter(Owners=['self'], Filters=Filters)
        except Exception as e:
            print('error: failed to list amis')
            print(e)
            self.amis = []
        return self

    def expired(self, days_old=15):
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

    def delete(self, DryRun=True):
        for ami in self.delete_amis:
            try:
                ami.deregister(DryRun)
                print('success: deleted ami (dryrun=%s) : %s ' % (DryRun, ami.id))
            except Exception as e:
                print('error: failed to delete ami %s: %s' % (ami.id, e))
