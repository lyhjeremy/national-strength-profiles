# National Strength Profiles — Who's Good at What

**Which countries are good at which athletic disciplines — and which archetypes do they cluster into?**

> 🌐 **Overview:** https://lyhjeremy.github.io/national-strength-profiles/

Olympic medal counts are a crude measure of national strength: they ignore the 99%
of elite performances that don't reach a podium. Using **WA points as a common
currency**, this project builds a country × discipline matrix of *athletic capital*
from **6,400 top performances (16 events, 2023–24)**, then clusters nations into
archetypes and maps them.

<p align="center">
  <img src="figures/archetypes_map.png" alt="PCA map of national athletics archetypes" width="820">
</p>

## What it finds

Clustering 43 nations on their WA-point strength across five discipline groups
(sprints, middle, distance, jumps, throws) yields five clean archetypes:

- **All-round powerhouses** — USA, Great Britain, Netherlands, Italy, Jamaica, Canada.
  The USA is a *massive* outlier: on the first principal component (overall depth) it
  sits far beyond everyone else.
- **Distance specialists** — Kenya, Uganda, Ireland: elite at distance and middle
  distance, and pointedly narrow.
- **Throw & jump powers** — Poland, China, Cuba, Nigeria and others whose strength is
  concentrated in the field events.
- **Distance & middle powers** — Australia, France, Germany, Norway, Japan, Spain: broad,
  established programmes with an endurance lean.
- **Emerging / single-event nations** — strong in one niche (a Bahamas 400 m, a
  Trinidad sprint) but not yet broad.

The two principal components read cleanly as **overall depth (PC1)** and a
**sprint/power ↔ distance axis (PC2)** — Kenya anchors one pole, the throws-and-jumps
nations the other.

## Run it
```bash
pip install -r requirements.txt
python fetch_data.py      # scrape WA top lists (mark + points + nationality) -> data/raw/
python analyze.py         # country × discipline matrix, KMeans + PCA -> figures/ + tables/
```

## Files
| Path | What it is |
|---|---|
| `fetch_data.py` | Scrape World Athletics top lists with nationality + WA points |
| `analyze.py` | Build the strength matrix, cluster nations (KMeans), map them (PCA) |
| `figures/` | Archetype map, discipline-strength heatmap, cluster fingerprints |
| `tables/` | `national_profiles.csv` (each nation's per-discipline strength + archetype) |

## Method notes
Strength per (nation, discipline) is the mean of a nation's **top-5 WA scores** in
that group — robust to one-off performances, representative of genuine depth. A
nation absent from a discipline is treated as having no elite presence (filled to
the column minimum) before z-scoring. Per-capita and per-GDP "overperformer" views
(Jamaica, Norway) are a natural next layer on top of this absolute matrix.

## License
[MIT](LICENSE) © 2026 Jeremy Lee · performance data from World Athletics top lists
