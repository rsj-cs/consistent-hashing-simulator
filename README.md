# Consistent Hashing Simulator

A Python implementation of consistent hashing — a core distributed systems algorithm used in systems like Amazon DynamoDB, Apache Cassandra, and Redis clusters.

## What is Consistent Hashing?

Consistent hashing is a technique that minimizes key reassignment when nodes are added or removed from a distributed cluster. Unlike traditional hashing, where adding a node reshuffles nearly all keys, consistent hashing only moves a fraction of keys — making it ideal for distributed caches and databases.

## Features

- Virtual node support for balanced key distribution
- Dynamic node addition and removal
- Automatic key redistribution on cluster changes
- Node failure simulation
- Visual distribution reports with bar charts

## How It Works

Keys and nodes are both mapped onto a circular hash ring using MD5 hashing. Each key is assigned to the first node encountered clockwise on the ring. Virtual nodes (replicas of each server) ensure even distribution even with few physical nodes.

## Sample Output
```
[1] Building initial cluster (3 nodes):
  [+] Node 'Server-A' added (3 virtual nodes)
  [+] Node 'Server-B' added (3 virtual nodes)
  [+] Node 'Server-C' added (3 virtual nodes)

[2] Key distribution across 100 keys:
  Server-A     | #######################      43 keys (43.0%)
  Server-B     | #################            35 keys (35.0%)
  Server-C     | ###########                  22 keys (22.0%)

[3] Scaling up — adding Server-D:
  Server-A     | ###############              30 keys (30.0%)
  Server-B     | ##########                   20 keys (20.0%)
  Server-C     | ##########                   19 keys (19.0%)
  Server-D     | ##############               31 keys (31.0%)

Keys reassigned after adding node: ~31 / 100
```

## Concepts Demonstrated

- Consistent hashing algorithm and ring topology
- Virtual nodes for uniform load distribution
- Fault tolerance through automatic key reassignment
- Scalability with minimal disruption on cluster changes

## Technologies

- Python 3.x
- `hashlib` for MD5-based ring placement
- `bisect` for O(log n) ring traversal

## Related Projects

- [Multithreaded Pipeline Benchmark](https://github.com/rsj-cs/multithreaded-pipeline-benchmark)
- [Data Validation Pipeline](https://github.com/rsj-cs/data-validation-pipeline)
- [Distributed Pipeline Capstone](https://github.com/rsj-cs/distributed-pipeline-capstone)
