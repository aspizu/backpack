create-benchmark-registry:
    bun tools/index.ts

benchmark:
    cargo run --release purge --all && cargo run --release sync ~/registry/pkg_m6761npi

flamegraph:
    cargo run --release purge --all && cargo flamegraph --freq 150 -- sync ~/registry/pkg_m6761npi
