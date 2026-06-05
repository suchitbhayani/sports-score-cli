import argparse
import sys

from sports_score_cli.api import ScoreboardError, fetch_scoreboard
from sports_score_cli.format import format_scoreboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sports-score",
        description="Fetch live NBA and NFL scores from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    live_parser = subparsers.add_parser(
        "live",
        help="Show live scores for a league",
    )
    live_parser.add_argument(
        "league",
        choices=["nba", "nfl"],
        help="League to fetch scores for",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "live":
        try:
            games = fetch_scoreboard(args.league)
        except ScoreboardError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        print(format_scoreboard(games, args.league))


if __name__ == "__main__":
    main()
