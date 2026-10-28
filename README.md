# controlla

Lightweight command-line interface for inspecting, managing, and tailing container processes across Docker and Podman runtimes.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Runtimes: Docker & Podman](https://img.shields.io/badge/engine-Docker%20%7C%20Podman-blue.svg)](#)

---

## Features

- **Dual-Engine Auto-Discovery**: Detects and binds to active `docker` or `podman` binary automatically.
- **Clean Table Formatting**: Clear terminal inspection of container names, IDs, statuses, and port mappings.
- **JSON Serialization**: Full support for `--json` output across query commands.
- **Process Lifecycle Operations**: Run, stop, inspect logs, and remove containers with simple subcommands.

---

## Quickstart

### 1. List Running Containers
```bash
python3 main.py ps
python3 main.py ps -a --json
```

### 2. Run a New Container
```bash
python3 main.py run --name redis_cache --image redis:alpine -p 6379:6379
```

### 3. Inspect Container Logs
```bash
python3 main.py logs redis_cache -n 100
```

### 4. Stop and Remove
```bash
python3 main.py stop redis_cache
python3 main.py rm -f redis_cache
```

---

## Testing

Run unit tests with subprocess mocks:
```bash
python3 -m unittest discover -s tests
```

---

## License

[MIT License](LICENSE)
