# Controlla (`controlla`)

> **Clean, fast container & process orchestration CLI.**  


[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mak74ik/controlla/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 Overview

`Controlla` is an agent-native CLI for inspecting, managing, running, and tailing container logs across Docker and Podman runtimes with clean tabular formatting and JSON output support.

---

## 🚀 Usage

### 1. List Containers
```bash
python3 main.py ps
python3 main.py ps -a --json
```

### 2. Run Container
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

## 🧪 Testing

Run automated unit tests:
```bash
python3 -m unittest discover -s tests
```

---

## 👥 Credits

Created & maintained by [Yoshi](https://github.com/mak74ik)
- 📦 **Runtime**: Docker / Podman Engine Integration
- 🛡️ **Quality Assurance**: Automated Subprocess Mock Regressions
