# National strength profiles: who's good at what

*Medal tables count the podium. WA points can describe the whole shape of a nation's athletics strength, and nations can be clustered by that shape.*

## Beyond the medal table

A medal count tells you a country won three golds. It can't tell you whether the country is a narrow specialist or strong everywhere, whether its strength is in sprinting or throwing, or how it does in the large majority of world-class performances that never reach a podium. World Athletics points put every performance in every event on one scale, so I used them as a measure of a nation's elite depth.

From 6,400 top performances (the top 100 in each of 16 events, men and women, 2023 and 2024, each with a nationality and a WA score) I built a country by discipline matrix. Each cell is a nation's mean top-five score in one of five groups: sprints, middle distance, distance, jumps and throws. Nations with presence in at least three groups and at least 12 performances make the cut, which leaves 43. K-means clustering then sorts the nations, and PCA maps them.

## Five archetypes

<p align="center">
  <img src="figures/archetypes_map.png" alt="PCA scatter of 43 nations colored by archetype. The USA sits alone at the far right of the first component; Kenya, Uganda and Ireland sit far below the rest on the second component." width="760">
</p>

The clusters are close to the ones a fan would name. Six all-round powerhouses (the USA, Great Britain, the Netherlands, Italy, Jamaica and Canada) are above average in every group, and even among them the USA stands apart: it scores 5.0 on the first principal component, against 2.8 for Great Britain and between 1.7 and 2.2 for the other four, and its summed strength is 242 points ahead of Great Britain's.

At the other corner of the map are the three distance specialists, Kenya, Uganda and Ireland. Kenya has the highest distance and middle-distance scores of any nation and sits at the bottom of the map on its own. Ten more nations (Australia, France, Germany, Norway, South Africa, Spain, Sweden, Japan, Belgium and Switzerland) form a group of distance and middle powers: broad programs with an endurance lean.

The largest cluster is the sixteen throw and jump powers, among them Poland, New Zealand, Cuba, China and Nigeria, which on average sit a little above the field in jumps and throws and below it on the track. The last eight are emerging or single-event nations, where one group stands out and there is little behind it: sprints for the Bahamas and Trinidad and Tobago, middle distance for Algeria.

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

Two modeling choices shape the result. A nation with no score in a group gets the column minimum, which is a reasonable reading of "no elite presence" but is still an imputation. And the top-five mean protects against one freak mark while underrating a country whose strength in a group is one athlete.

The cluster boundaries are soft. Rerunning k-means on the committed table with scikit-learn 1.6 moves three nations: Germany and South Africa join the all-rounders and Mexico joins the emerging group. A re-fetch of the raw top lists also once gave values that differed from the committed table, and I never found out why. The numbers here are the ones in `tables/national_profiles.csv`.

*Code: [github.com/lyhjeremy/national-strength-profiles](https://github.com/lyhjeremy/national-strength-profiles)*
