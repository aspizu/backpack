create-benchmark-registry:
    bun tools/index.ts

benchmark:
    rm -rf ~/.cache/backpack && cargo run --release sync ~/registry/pkg_m6761npi

flamegraph:
    rm -rf ~/.cache/backpack && cargo flamegraph --freq 150 -- sync ~/registry/pkg_m6761npi
