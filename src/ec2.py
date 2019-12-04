import boto3
from botocore.client import Config
import arrow

class EC2:

    def __init__(self):
        self.ec2 = boto3.resource('ec2', config=Config(region_name="ap-southeast-2"))
        self.now = arrow.utcnow()

    def get_delete_time(self, days=15):
        return self.now.shift(days=-days).datetime

    def list(self, Filters=[]):
        pass

    def expired(self, days_old=15):
        pass

    def delete(self, DryRun=True):
        pass
