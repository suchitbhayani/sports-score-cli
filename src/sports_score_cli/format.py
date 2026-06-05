"""Format scoreboard data for terminal output."""

from sports_score_cli.api import Game, TeamScore

STATE_ORDER = {"in": 0, "pre": 1, "post": 2}
STATE_LABELS = {
    "in": "LIVE",
    "pre": "UPCOMING",
    "post": "FINAL",
}


def _format_period(period: int) -> str:
    if period <= 4:
        return f"Q{period}"
    return "OT"


def _format_team(team: TeamScore) -> str:
    winner = "*" if team.is_winner else " "
    return f"{winner}{team.abbreviation:>3} {team.score:>3}"


def _format_status(game: Game) -> str:
    if game.state == "in" and game.period:
        period = _format_period(game.period)
        clock = game.clock or ""
        return f"{period} {clock}".strip()
    if game.state == "post":
        return "Final"
    return game.status_detail


def format_game(game: Game) -> str:
    label = STATE_LABELS.get(game.state, game.status.upper())
    matchup = f"{_format_team(game.away)} @ {_format_team(game.home)}"
    status = _format_status(game)
    return f"[{label:<8}] {matchup}  {status}"


def format_scoreboard(games: list[Game], league: str) -> str:
    if not games:
        return f"No {league.upper()} games on the scoreboard right now."

    sorted_games = sorted(
        games,
        key=lambda game: (STATE_ORDER.get(game.state, 3), game.name),
    )

    header = f"{league.upper()} Scoreboard"
    divider = "=" * len(header)
    lines = [header, divider, ""]
    lines.extend(format_game(game) for game in sorted_games)

    live_count = sum(1 for game in games if game.state == "in")
    if live_count:
        lines.extend(["", f"{live_count} game(s) in progress"])

    return "\n".join(lines)
