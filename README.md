pyHacks (Rust rewrite)
======================

This repository now provides a Rust implementation of the original port scanner script.

## Build

```bash
cargo build --release
```

## Usage

```bash
cargo run -- <hostname-or-ip>
```

The scanner checks TCP ports 1 through 65535 and reports each as open or closed.
