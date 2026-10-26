# National strength profiles: who's good at what

*Medal tables count the podium. WA points can describe the whole shape of a nation's athletics strength, and nations can be clustered by that shape.*

## Beyond the medal table

A medal count tells you a country won three golds. It doesn't say whether the country is a narrow specialist or strong everywhere, whether its strength is in sprinting or throwing, or how it does in the large majority of world-class performances that never reach a podium. World Athletics points put every performance in every event on one scale, so I used them as a measure of a nation's elite depth.

From 6,400 top performances (the top 100 in each of 16 events, men and women, 2023 and 2024, each with a nationality and a WA score) I built a country by discipline matrix. Each cell is a nation's mean top-five score in one of five groups: sprints, middle distance, distance, jumps and throws. Nations with presence in at least three groups and at least 12 performances make the cut, which leaves 43. Then k-means clustering sorts the nations and PCA maps them.

## Five archetypes

<p align="center">
  <img src="figures/archetypes_map.png" alt="PCA scatter of 43 nations coloured by archetype. The USA sits alone at the far right of the first component; Kenya, Uganda and Ireland sit far below the rest on the second component." width="760">
</p>

The clusters are close to the ones a fan would name:

- **All-round powerhouses:** the USA, Great Britain, the Netherlands, Italy, Jamaica and Canada. All are above average in every group. The USA stands apart even here: it scores 5.0 on the first principal component, Great Britain 2.8, and the other four between 1.7 and 2.2. Its summed strength is 242 points ahead of Great Britain's.
- **Distance specialists:** Kenya, Uganda and Ireland. Kenya has the highest distance and middle-distance scores of any nation and sits at the bottom of the map on its own.
- **Distance and middle powers:** Australia, France, Germany, Norway, South Africa, Spain, Sweden, Japan, Belgium and Switzerland. Broad programmes with an endurance lean.
- **Throw and jump powers:** sixteen nations including Poland, New Zealand, Cuba, China and Nigeria. On average a little above the field in jumps and throws and below it on the track.
- **Emerging or single-event nations:** eight, including the Bahamas and Trinidad and Tobago (sprints) and Algeria (middle distance). One group stands out and there is little behind it.

<p align="center">
  <img src="figures/strength_heatmap.png" alt="Heatmap of 28 nations against five discipline groups, z-scored and grouped by archetype, with strong cells in red and weak cells in blue." width="620">
</p>

## What the axes mean

The two principal components explain 78% of the variance between them. PC1 (49%) loads almost evenly on all five groups, so it is overall depth: it runs from the emerging nations up to the USA. PC2 (29%) loads positively on jumps and throws and negatively on distance and middle distance, so it separates field-event nations (top of the map) from endurance nations (bottom). Kenya, Uganda and Ireland sit at the bottom of that axis.

<p align="center">
  <img src="figures/archetype_fingerprints.png" alt="Grouped bar chart of each archetype's mean z-scored strength in the five discipline groups. Distance specialists are high on distance and very low on jumps and throws; all-rounders are positive everywhere." width="720">
</p>

Each cluster has a fingerprint. The distance specialists are well above average on distance (mean z of 1.5) and far below it on jumps (−2.0). The all-rounders are positive in every group. The throw and jump powers are mildly positive in the field and negative on the track.

## Limits and next steps

The matrix measures absolute strength. Dividing it by population or GDP would give a different map of overperformers, with Jamaica and Norway as likely candidates, and that is the obvious next layer.

Two modelling choices matter. A nation with no score in a group gets the column minimum, which is a reasonable reading of "no elite presence" but is still an imputation. And the top-five mean protects against one freak mark while underrating a country whose strength in a group is one athlete.

The cluster boundaries are soft. Rerunning k-means on the committed table with scikit-learn 1.6 moves three nations: Germany and South Africa join the all-rounders and Mexico joins the emerging group. A re-fetch of the raw top lists also once gave values that differed from the committed table, and I never found out why. The numbers here are the ones in `tables/national_profiles.csv`.

*Code: [github.com/lyhjeremy/national-strength-profiles](https://github.com/lyhjeremy/national-strength-profiles)*
