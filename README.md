# ebs-cleaner

A scheduled lambda to clean EBS snapshots.
Allow the use of filtering by tags and age.
Run as a local command or as a lambda.

Example of using tag filter.
```
python3 ./index.py -filters='[{"Name": "tag:Name", "Values": [ "oldUn*"]}]'
```

