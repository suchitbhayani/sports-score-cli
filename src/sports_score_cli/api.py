"""ESPN API client for fetching sports scores."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ESPN_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports"


class League(str, Enum):
    NBA = "nba"
    NFL = "nfl"


LEAGUE_PATHS: dict[League, str] = {
    League.NBA: "basketball/nba",
    League.NFL: "football/nfl",
}


@dataclass(frozen=True)
class TeamScore:
    name: str
    abbreviation: str
    score: str
    is_home: bool
    is_winner: bool | None


@dataclass(frozen=True)
class BettingLines:
    provider: str
    spread_detail: str | None
    over_under: float | None
    home_moneyline: str | None
    away_moneyline: str | None


@dataclass(frozen=True)
class Game:
    name: str
    short_name: str
    status: str
    status_detail: str
    state: str
    clock: str | None
    period: int | None
    home: TeamScore
    away: TeamScore
    betting_lines: BettingLines | None


class ScoreboardError(Exception):
    """Raised when the scoreboard cannot be fetched or parsed."""


def _parse_team(competitor: dict[str, Any]) -> TeamScore:
    team = competitor["team"]
    return TeamScore(
        name=team["displayName"],
        abbreviation=team["abbreviation"],
        score=str(competitor.get("score", "0")),
        is_home=competitor["homeAway"] == "home",
        is_winner=competitor.get("winner"),
    )


def _parse_betting_lines(competition: dict[str, Any]) -> BettingLines | None:
    odds_list = competition.get("odds")
    if not odds_list:
        return None

    odds = odds_list[0]
    provider_info = odds.get("provider", {})
    provider = provider_info.get("displayName") or provider_info.get("name", "Unknown")
    moneyline = odds.get("moneyline", {})

    return BettingLines(
        provider=provider,
        spread_detail=odds.get("details"),
        over_under=odds.get("overUnder"),
        home_moneyline=moneyline.get("home", {}).get("close", {}).get("odds"),
        away_moneyline=moneyline.get("away", {}).get("close", {}).get("odds"),
    )


def _parse_game(event: dict[str, Any]) -> Game:
    competition = event["competitions"][0]
    status = competition["status"]
    status_type = status["type"]
    competitors = competition["competitors"]

    home = next(c for c in competitors if c["homeAway"] == "home")
    away = next(c for c in competitors if c["homeAway"] == "away")

    state = status_type["state"]
    clock = status.get("displayClock") if state == "in" else None
    period = status.get("period") if state == "in" else None

    return Game(
        name=event["name"],
        short_name=event["shortName"],
        status=status_type["description"],
        status_detail=status_type.get("shortDetail", status_type["description"]),
        state=state,
        clock=clock,
        period=period,
        home=_parse_team(home),
        away=_parse_team(away),
        betting_lines=_parse_betting_lines(competition),
    )


def fetch_scoreboard(league: League | str) -> list[Game]:
    """Fetch today's scoreboard for the given league."""
    try:
        league = League(league)
    except ValueError as exc:
        supported = ", ".join(league.value for league in League)
        raise ScoreboardError(
            f"Unsupported league '{league}'. Supported leagues: {supported}."
        ) from exc

    url = f"{ESPN_BASE_URL}/{LEAGUE_PATHS[league]}/scoreboard"
    request = Request(url, headers={"User-Agent": "sports-score-cli/0.1.0"})

    try:
        with urlopen(request, timeout=10) as response:
            data = json.load(response)
    except HTTPError as exc:
        raise ScoreboardError(f"ESPN API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise ScoreboardError(f"Failed to reach ESPN API: {exc.reason}.") from exc
    except json.JSONDecodeError as exc:
        raise ScoreboardError("ESPN API returned invalid JSON.") from exc

    events = data.get("events", [])
    return [_parse_game(event) for event in events]
