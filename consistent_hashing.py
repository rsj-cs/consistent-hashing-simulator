import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, virtual_nodes=3):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}#vnode{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)
        print(f"  [+] Node '{node}' added ({self.virtual_nodes} virtual nodes)")

    def remove_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}#vnode{i}"
            hash_val = self._hash(virtual_key)
            self.ring.pop(hash_val, None)
            if hash_val in self.sorted_keys:
                self.sorted_keys.remove(hash_val)
        print(f"  [-] Node '{node}' removed")

    def get_node(self, key):
        if not self.ring:
            return None
        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def get_distribution(self, keys):
        distribution = {}
        for key in keys:
            node = self.get_node(key)
            distribution[node] = distribution.get(node, 0) + 1
        return distribution


def print_distribution(distribution, total):
    for node, count in sorted(distribution.items()):
        pct = count / total * 100
        bar = "#" * int(pct / 2)
        print(f"  {node:<12} | {bar:<25} {count:>4} keys ({pct:.1f}%)")


if __name__ == "__main__":
    print("=" * 55)
    print("   CONSISTENT HASHING - DISTRIBUTED SYSTEMS DEMO")
    print("=" * 55)

    ring = ConsistentHashRing(virtual_nodes=3)

    print("\n[1] Building initial cluster (3 nodes):")
    ring.add_node("Server-A")
    ring.add_node("Server-B")
    ring.add_node("Server-C")

    keys = [f"user:{i}" for i in range(1, 101)]

    print("\n[2] Key distribution across 100 keys:")
    dist = ring.get_distribution(keys)
    print_distribution(dist, len(keys))

    print("\n[3] Scaling up — adding Server-D:")
    ring.add_node("Server-D")
    new_dist = ring.get_distribution(keys)
    print_distribution(new_dist, len(keys))

    moved = sum(
        1 for k in keys
        if ring.get_node(k) != ConsistentHashRing(virtual_nodes=3)
        .__class__(virtual_nodes=3) or True
    )
    reassigned = sum(
        abs(new_dist.get(n, 0) - dist.get(n, 0))
        for n in set(list(dist) + list(new_dist))
    ) // 2
    print(f"\n  Keys reassigned after adding node: ~{reassigned} / {len(keys)}")

    print("\n[4] Node failure simulation — removing Server-B:")
    ring.remove_node("Server-B")
    fail_dist = ring.get_distribution(keys)
    print_distribution(fail_dist, len(keys))

    print("\n[5] Specific key lookups:")
    test_keys = ["user:42", "session:abc123", "cache:homepage", "db:record_99"]
    for k in test_keys:
        print(f"  '{k}' -> {ring.get_node(k)}")

    print("=" * 55)
    print("  Consistent hashing minimizes key reassignment")
    print("  when nodes are added or removed from the cluster.")
    print("=" * 55)