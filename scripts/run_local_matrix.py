from __future__ import annotations

import argparse
import time
import tomllib

from common import (
    ROOT,
    require_executable,
    run_command,
    save_json,
    stratified_map_seed_pairs,
    stratified_screen_side_swaps,
    utc_run_id,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default=None)
    parser.add_argument("--baseline", default=None)
    parser.add_argument("--config", default="configs/eval_matrix.toml")
    parser.add_argument("--maps", nargs="*")
    parser.add_argument("--seeds", nargs="*", type=int)
    parser.add_argument("--limit", type=int, help="Limit games for a smoke run.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_executable("fcode")

    config_path = ROOT / args.config
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    candidate = args.candidate or config["candidate"]
    baseline = args.baseline or config["baseline"]
    maps = args.maps or config["maps"]
    seeds = args.seeds or config["seeds"]
    tle_ms = int(config.get("tle_ms", 10))
    side_swap = bool(config.get("side_swap", True))
    screen_seed = config.get("screen_seed")
    screen_side_swaps = None
    if screen_seed is not None:
        schedule = stratified_map_seed_pairs(
            maps,
            seeds,
            int(config.get("screen_pairs", 27)),
            int(screen_seed),
        )
        if "screen_games" in config:
            screen_side_swaps = stratified_screen_side_swaps(
                len(schedule),
                int(config["screen_games"]),
                int(screen_seed),
                side_swap=side_swap,
            )
    else:
        schedule = [(map_name, seed) for map_name in maps for seed in seeds]

    run_id = utc_run_id("local")
    report_dir = ROOT / "reports" / run_id
    replay_dir = report_dir / "replays"
    replay_dir.mkdir(parents=True, exist_ok=True)

    records = []
    game_no = 0
    stop = False
    for pair_index, (map_name, seed) in enumerate(schedule):
        orders = [(candidate, baseline, "candidate-A")]
        if side_swap and (screen_side_swaps is None or pair_index in screen_side_swaps):
            orders.append((baseline, candidate, "candidate-B"))
        for bot_a, bot_b, side in orders:
            game_no += 1
            if args.limit and game_no > args.limit:
                stop = True
                break
            replay = replay_dir / f"{game_no:04d}_{map_name}_s{seed}_{side}.replay26"
            argv = [
                "fcode", "run", bot_a, bot_b, map_name,
                "--seed", str(seed),
                "--tle", str(tle_ms),
                "--replay", str(replay),
                "--json",
            ]
            started = time.monotonic()
            result = run_command(argv)
            elapsed = time.monotonic() - started
            # Older CLI fallback if --json is unavailable.
            if result.returncode != 0 and "--json" in result.stderr and (
                "option" in result.stderr.lower() or "unexpected" in result.stderr.lower()
            ):
                argv.remove("--json")
                result = run_command(argv)
            record = result.to_dict()
            record.update({
                "game": game_no,
                "map": map_name,
                "seed": seed,
                "candidate_side": side,
                "candidate": candidate,
                "baseline": baseline,
                "elapsed_seconds": elapsed,
                "replay": str(replay.relative_to(ROOT)),
            })
            records.append(record)
            print(
                f"[{game_no}] {map_name} seed={seed} {side}: "
                f"rc={result.returncode} elapsed={elapsed:.2f}s"
            )
        if stop:
            break

    save_json(report_dir / "manifest.json", {
        "run_id": run_id,
        "candidate": candidate,
        "baseline": baseline,
        "maps": maps,
        "seeds": seeds,
        "schedule": [{"map": map_name, "seed": seed} for map_name, seed in schedule],
        "screen_seed": screen_seed,
        "screen_side_swapped_pairs": (
            len(screen_side_swaps) if screen_side_swaps is not None else None
        ),
        "tle_ms": tle_ms,
        "side_swap": side_swap,
        "games_requested": game_no if not args.limit else min(game_no, args.limit),
    })
    save_json(report_dir / "games.json", records)

    failures = [r for r in records if r["returncode"] != 0]
    print(f"\nReport: {report_dir}")
    print(f"Games: {len(records)}, command failures: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
