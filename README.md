# Merkle root for EVM
A simple merkle root generator script, which takes keccak256 hashes from a csv file and create a merkle root from them, which can be used in EVM applications (for example for airdrops)

The script generates a file with the merkle root, parents, and siblings, which can be then used to construct a path from leaf to the root. Siblings file is mapping from each node to its sibling (since Merkle root is a complete binary tree each node has exactly one sibling). Parents file is mapping from each node to its parent.
