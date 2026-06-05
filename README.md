# Sports Score CLI

A command-line tool for fetching live NBA and NFL scores without opening a browser.
It pulls data from ESPN's public API and displays games grouped by status — live,
upcoming, and final — with scores, game clocks, and start times.

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
```

Games in progress are labeled `LIVE` and show the current quarter and clock.
Completed games are labeled `FINAL`, and the winning team is marked with `*`.

You can also run the tool from a local clone without installing globally:

```bash
uv run sports-score live nba
```
