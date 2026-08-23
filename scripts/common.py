from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import random
import shutil
import subprocess
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]


def utc_run_id(prefix: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{stamp}"


@dataclass
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str

    def to_dict(self) -> dict:
        parsed = None
        try:
            parsed = json.loads(self.stdout)
        except json.JSONDecodeError:
            pass
        return {
            "argv": self.argv,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "json": parsed,
        }


def require_executable(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required executable not found: {name}")
    return path


def run_command(argv: Sequence[str], *, cwd: Path = ROOT) -> CommandResult:
    env = dict(os.environ)
    env.setdefault("FCODE_NO_UPDATE_CHECK", "1")
    proc = subprocess.run(
        list(argv),
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return CommandResult(list(argv), proc.returncode, proc.stdout, proc.stderr)


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def stratified_map_seed_pairs(
    maps: Sequence[str],
    seeds: Sequence[int],
    pair_count: int,
    random_seed: int,
) -> list[tuple[str, int]]:
    """Build a reproducible, all-map screen schedule.

    The first selected pair for every map guarantees coverage; the remaining
    pairs come from the same seeded shuffle of the full map/seed pool. Keeping
    the schedule explicit in the matrix manifest makes a randomized screen
    auditable and repeatable while allowing the seed to rotate per iteration.
    """
    unique_maps = list(dict.fromkeys(maps))
    unique_seeds = list(dict.fromkeys(int(seed) for seed in seeds))
    if not unique_maps or not unique_seeds:
        raise ValueError("screen schedule requires at least one map and seed")
    if pair_count < len(unique_maps):
        raise ValueError("pair_count must cover every map at least once")
    pool = [(map_name, seed) for map_name in unique_maps for seed in unique_seeds]
    if pair_count > len(pool):
        raise ValueError("pair_count exceeds the available map/seed pool")
    random.Random(random_seed).shuffle(pool)
    selected: list[tuple[str, int]] = []
    covered: set[str] = set()
    for pair in pool:
        if pair[0] in covered:
            continue
        selected.append(pair)
        covered.add(pair[0])
        if len(covered) == len(unique_maps):
            break
    selected_set = set(selected)
    selected.extend(pair for pair in pool if pair not in selected_set)
    return selected[:pair_count]


def stratified_screen_side_swaps(
    pair_count: int,
    game_count: int,
    random_seed: int,
    *,
    side_swap: bool,
) -> set[int]:
    """Choose which all-map screen pairs receive the second side order.

    A screen must run at least one game for every selected map pair.  When a
    smaller-than-full screen is requested, a seeded subset receives the second
    order so map coverage is retained while side coverage rotates between
    iterations.  The returned indices are stable for a given screen seed.
    """
    if pair_count <= 0:
        raise ValueError("screen requires at least one map/seed pair")
    if not side_swap:
        if game_count != pair_count:
            raise ValueError("without side swaps, game_count must equal pair_count")
        return set()
    if game_count < pair_count or game_count > pair_count * 2:
        raise ValueError("screen game_count must be between pair_count and 2*pair_count")
    extra_pairs = game_count - pair_count
    return set(random.Random(random_seed ^ 0x5EED).sample(range(pair_count), extra_pairs))
