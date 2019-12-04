## ebs-ami-cleaner [![CircleCI](https://circleci.com/gh/wrasdf/snapshot-cleaner/tree/master.svg?style=svg)](https://circleci.com/gh/wrasdf/snapshot-cleaner/tree/master)

Local docker to clean EBS snapshots & AMI images.
Allow the use of filtering by tags and age.


#### Example of using tag filter.
AWS auth first

```
make sh
python ./index.py -type=snapshot -filters='[{"Name": "tag:Name", "Values": [ "kubernetes-dynamic-pvc*"]}]'  -age=30 -dryrun=false
python ./index.py -type=ami -filters='[{"Name": "tag:CreatedBy", "Values": [ "ops-kube-redwine"]}]' -age=30 -dryrun=false
```

#### Tests
```
make test
```
