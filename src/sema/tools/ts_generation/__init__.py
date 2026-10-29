"""Generation of the TypeScript sema runtime: one zod schema per word.

A sibling of ``runtime_generation`` (the Python runtime). Both read the same
seed DAG and definitions; this package writes the TypeScript a browser vendors
as its snapshot.
"""
