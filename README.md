# National strength profiles

Which countries are good at which athletics disciplines: k-means and PCA on WA-point strength for 43 nations, built from 6,400 elite performances.

[Live site](https://lyhjeremy.github.io/national-strength-profiles/) · [Write-up](https://lyhjeremy.github.io/national-strength-profiles/overview/) · [Long-form notes](writeup.md)

Design and copy follow [these standards](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md).

## Results

- 43 nations cluster into five archetypes: all-round powerhouses (6), distance specialists (3), distance and middle powers (10), throw and jump powers (16), and emerging or single-event nations (8).
- Two principal components explain 78% of the variance: overall depth (PC1, 49%) and field events against endurance (PC2, 29%).
- The USA scores 5.0 on PC1; Great Britain is next at 2.8. The USA has the highest strength score in sprints, jumps and throws, and Kenya leads middle distance and distance.

<p align="center">
  <img src="figures/archetypes_map.png" alt="PCA scatter of 43 nations coloured by archetype. The USA sits alone at the far right of the first component; Kenya, Uganda and Ireland sit far below the rest on the second component." width="820">
</p>

## Method

1. `fetch_data.py` scrapes the World Athletics outdoor top lists: top 100 per event for 16 events, men and women, 2023 and 2024 (6,400 performances), each with its mark, nationality and WA points ("Results Score").
2. Events are grouped into sprints, middle distance, distance, jumps and throws. A nation's strength in a group is the mean of its top five WA scores there, given at least three performances in that group.
3. Nations need presence in at least three groups and 12 performances overall, which leaves 43. A missing group is filled with the column minimum (no elite presence), then each column is z-scored with `StandardScaler`.
4. K-means (k = 5, `random_state=0`) assigns archetypes. Each cluster is named by rule from its mean z-profile, for example "specialists" when one group clearly dominates.
5. PCA projects the five z-scores onto two axes for the map.

## Stack

Python, pandas, lxml, NumPy, scikit-learn, matplotlib. Static site on GitHub Pages.

## How to run

```bash
pip install -r requirements.txt
python fetch_data.py      # scrape WA top lists (mark, points, nationality) -> data/raw/ (git-ignored)
python analyze.py         # strength matrix, k-means and PCA -> figures/ and tables/
```

## Repo layout

| Path | What it is |
|---|---|
| `fetch_data.py` | Scrape World Athletics top lists with nationality and WA points |
| `analyze.py` | Build the strength matrix, cluster nations (k-means), map them (PCA) |
| `figures/` | Archetype map, strength heatmap, cluster fingerprints |
| `tables/national_profiles.csv` | Each nation's five strength scores, total and archetype |
| `index.html`, `overview/` | The two pages of the site |
| `writeup.md` | Long-form notes |

## Limitations

- This is absolute strength. Large countries do well by construction; there is no per-capita or per-GDP view yet.
- Filling a missing group with the column minimum is an imputation, and it pushes the specialist clusters apart.
- Averaging the top five protects against one-off marks but undersells a country with a single world-beater in a group.
- Borderline assignments are not stable. Rerunning k-means on the committed table with scikit-learn 1.6 moves Germany and South Africa to the all-rounders and Mexico to the emerging group. A re-fetch of the raw top lists also once gave values different from the committed table, and the cause was not found.

## License

[MIT](LICENSE) © 2026 Jeremy Lee. Performance data from World Athletics top lists.
