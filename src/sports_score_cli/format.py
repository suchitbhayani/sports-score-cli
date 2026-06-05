"""Format scoreboard data for terminal output."""

from sports_score_cli.api import Game


def format_game(game: Game) -> str:
    away = game.away
    home = game.home
    return (
        f"{away.abbreviation} {away.score} @ {home.abbreviation} {home.score}"
        f"  [{game.status_detail}]"
    )


def format_scoreboard(games: list[Game], league: str) -> str:
    if not games:
        return f"No {league.upper()} games found for today."

    header = f"{league.upper()} Scoreboard"
    lines = [header, "-" * len(header)]
    lines.extend(format_game(game) for game in games)
    return "\n".join(lines)
