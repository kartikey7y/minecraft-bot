# DreamBot — Python Mineflayer Agent

DreamBot is a **Python-first** Minecraft AI agent that targets the Mineflayer
ecosystem while keeping all orchestration, strategy, and tooling in Python. The
goal is to build a pro-level survival bot that can connect over LAN and run
autonomously with clear, testable behavior loops.

## Highlights
- **Python-only control plane** with a clean, typed architecture.
- **LAN connectivity validation** before boot.
- **Behavior engine** with a planner/critic loop.
- **uv package manager** support for fast, reproducible environments.

## Requirements
- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv)
- A Mineflayer-compatible environment (LAN server or local instance).

## Quick start (uv)
```bash
uv venv
uv pip install -e .
uv run dreambot --host 192.168.1.10 --port 25565 --username DreamBot
```

## What is implemented
DreamBot ships a production-grade foundation:
- LAN connectivity checks with clear failure messages.
- A modular agent loop (plan → act → observe → reflect → learn).
- A strategy brain that reacts to health, hunger, threats, and time of day.
- A memory store for long-term lessons.

## Next steps
Hook the Mineflayer adapter to your preferred Mineflayer-compatible runtime.
DreamBot is designed so the adapter is the only surface that must integrate
with the underlying Minecraft protocol or Mineflayer API.
