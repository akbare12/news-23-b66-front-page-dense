# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b66-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b66-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image front page summing up **Monday 23 November 2026** in world news:
the AI rout that hit Asia (Kospi −3.3%), Guterres' call to regulate AI before it's
too late, and the US lead over China at its record low — plus 28 more stories
across 6 regions, a world map with numbered pins, and a DATE CHECK box that
keeps 22 November's news out of the 23rd.

## How it is built

- `draw.py` (PIL) renders `entry.png` (1024×1024, < 1 MiB).
- `main.py` (stdlib only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies it byte-for-byte
  (PNG signature, IHDR 1024×1024, IEND trailer, ≤ 1 MiB).

## Stories (31)

**Heroes:** AI rout hits Asia · Guterres: regulate AI before it's too late ·
US lead over China at record low. **10 cards:** Bessent/Nvidia, FBI/NCIC hack,
Trump/Iran strikes, Nasdaq futures +3%, Skubal's $450M Mets deal, Tom Jackson
dies at 75, states sue SpaceX, Anthropic IPO $107.3B, Poland missile claim,
Russian nuclear satellite claim. **Also:** 18 more, from the Paris billionaire
tax to Seoul's 10T-won stabilisation fund.
