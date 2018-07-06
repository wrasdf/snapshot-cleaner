# ebs-cleaner

A scheduled lambda to clean EBS snapshots.
Allow the use of filtering by tags and age.

Example of using tag filter.
```
make sh
python ./index.py -filters='[{"Name": "tag:Name", "Values": [ "oldUn*"]}]'
```
