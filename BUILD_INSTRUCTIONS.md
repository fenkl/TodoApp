# Tauri Build Instructions

## Prerequisites
- Node.js (version 18 or higher)
- Rust (via rustup)

## Installation
If you're on an Arch-based distribution like Manjaro, make sure the following packages are installed:
```bash
sudo pacman -S nodejs npm rustup
```

Then install the Tauri CLI using cargo:
```bash
cargo install tauri-cli
```

Or if you already have rustup installed (which is common on Arch systems):
```bash
# Verify you have rustup installed
rustup --version

# Install Tauri CLI with cargo
cargo tauri --version
```

## Building the Project
To build your Tauri application:
```bash
npm run build
```

## Development
For development mode:
```bash
npm run dev
```