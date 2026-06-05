# Sports Score CLI

A command-line tool for fetching live NBA and NFL scores without opening a browser.
It pulls data from ESPN's public API and displays games grouped by status — live,
upcoming, and final — with scores, game clocks, start times, and betting lines
(spread, over/under, and moneyline) when available.

## Usage

Install the tool with uv:

```bash
uv add "git+https://github.com/suchitbhayani/sports-score-cli.git"
```

Show today's NBA scoreboard:

```bash
sports-score live nba
```

Show today's NFL scoreboard:

```bash
sports-score live nfl
```

Example output:

```
NBA Scoreboard
==============

[UPCOMING]   NY   0 @   SA   0  6/5 - 8:30 PM EDT
             Spread: SA -6.5 | O/U: 214.5 | ML: NY +180 / SA -218 | via Draft Kings
```

Games in progress are labeled `LIVE` and show the current quarter and clock.
Completed games are labeled `FINAL`, and the winning team is marked with `*`.
Betting lines are shown under each game when ESPN provides them.

You can also run the tool from a local clone without installing globally:

```bash
uv run sports-score live nba
```
