"""Command line entrypoint for DreamBot."""

from __future__ import annotations

import argparse
from pathlib import Path

from dreambot.adapter import MineflayerAdapter, NullAdapter
from dreambot.agent import DreamBot
from dreambot.memory import MemoryStore
from dreambot.net import connect_to_lan
from dreambot.strategy import StrategyBrain


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run DreamBot.")
    parser.add_argument("--host", default="127.0.0.1", help="LAN host or IP.")
    parser.add_argument("--port", type=int, default=25565, help="LAN port.")
    parser.add_argument("--username", default="DreamBot", help="Bot username.")
    parser.add_argument("--timeout", type=float, default=5.0, help="LAN timeout.")
    parser.add_argument(
        "--memory-path",
        default=".dreambot/memory.jsonl",
        help="Path to store long-term memory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without connecting to Mineflayer (strategy only).",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=None,
        help="Number of cycles to run before stopping.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.dry_run:
        result = connect_to_lan(args.host, args.port, args.timeout)
        if not result.success:
            print(f"[FAIL] {result.host}:{result.port} - {result.message}")
            return 1

    adapter = NullAdapter() if args.dry_run else MineflayerAdapter(
        host=args.host,
        port=args.port,
        username=args.username,
    )
    memory = MemoryStore(Path(args.memory_path))
    brain = StrategyBrain()

    bot = DreamBot(adapter=adapter, memory=memory, brain=brain)
    bot.run(cycles=args.cycles)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
