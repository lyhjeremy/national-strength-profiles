"""National strength profiles — which countries are good at what, and who clusters with whom.

Using WA points as a common currency, we build a country × event-category matrix of
"athletic capital": each cell is a nation's mean top-5 WA score in that discipline
group (sprints, middle, distance, jumps, throws). Then we cluster nations into
archetypes and map them, revealing the sprint powers, the distance powers, the
throw-and-jump powers, and the all-round machines.

Outputs: figures/*.png, tables/*.csv
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
FIG, TAB = ROOT / "figures", ROOT / "tables"
CATS = ["sprint", "middle", "distance", "jump", "throw"]
TOP_N = 5
MIN_CATS = 3          # a nation must have elite presence in at least this many categories
MIN_PERF = 12
K = 5
INK, GOLD, WINE = "#1a1a2e", "#D4A537", "#7a1f2b"
PALETTE = ["#7a1f2b", "#4a7ba6", "#2a7f62", "#c99a3b", "#6a4c93", "#b5651d"]


def build_matrix(df: pd.DataFrame) -> pd.DataFrame:
    # top-5 mean WA score per (nation, category)
    rows = []
    for (nat, cat), g in df.groupby(["nat", "category"]):
        if len(g) >= 3:
            rows.append({"nat": nat, "category": cat, "strength": g.score.nlargest(TOP_N).mean()})
    mat = pd.DataFrame(rows).pivot(index="nat", columns="category", values="strength")
    mat = mat.reindex(columns=CATS)
    counts = df.groupby("nat").size()
    keep = (mat.notna().sum(axis=1) >= MIN_CATS) & (counts.reindex(mat.index) >= MIN_PERF)
    mat = mat[keep]
    # absent category = no elite presence → fill with each column's observed minimum
    return mat.fillna(mat.min())


def main() -> None:
    FIG.mkdir(exist_ok=True); TAB.mkdir(exist_ok=True)
    df = pd.read_csv(ROOT / "data" / "raw" / "toplists.csv")
    mat = build_matrix(df)
    print(f"{len(mat)} nations profiled across {len(CATS)} categories "
          f"(from {df.nat.nunique()} nations, {len(df)} performances)")

    X = StandardScaler().fit_transform(mat.values)
    km = KMeans(n_clusters=K, n_init=10, random_state=0).fit(X)
    mat["cluster"] = km.labels_
    mat["total"] = mat[CATS].sum(axis=1)

    # name each cluster by the category it is (relatively) strongest in
    zmat = pd.DataFrame(X, index=mat.index, columns=CATS)
    zmat["cluster"] = km.labels_
    names = {}
    for c in range(K):
        prof = zmat[zmat.cluster == c][CATS].mean().sort_values(ascending=False)
        level, spread = prof.mean(), prof.std()
        if prof.iloc[0] < 0.15:                                  # not distinctly strong anywhere
            names[c] = "Emerging / single-event"
        elif level > 0.55 and spread < 0.55:                     # strong and balanced
            names[c] = "All-round powerhouses"
        elif prof.iloc[0] > 1.0 and spread > 0.8:                # elite but narrow
            names[c] = f"{prof.index[0].capitalize()} specialists"
        elif prof.iloc[0] - prof.iloc[1] > 0.55:                 # one category clearly dominates
            names[c] = f"{prof.index[0].capitalize()} specialists"
        else:                                                    # led by two disciplines
            names[c] = f"{prof.index[0].capitalize()} & {prof.index[1].capitalize()} powers"
    mat["archetype"] = mat.cluster.map(names)

    print("\nArchetypes:")
    for c in range(K):
        members = mat[mat.cluster == c].sort_values("total", ascending=False)
        print(f"  [{names[c]}]  {', '.join(members.index[:8])}"
              + (f"  (+{len(members)-8} more)" if len(members) > 8 else ""))

    print("\nStrongest overall (sum of category ceilings):")
    for nat, r in mat.sort_values("total", ascending=False).head(6).iterrows():
        print(f"  {nat}: {r.total:.0f}  [{r.archetype}]")

    mat.sort_values("total", ascending=False).to_csv(TAB / "national_profiles.csv")
    _figures(mat, zmat, X, km, names)


def _figures(mat, zmat, X, km, names):
    # Fig 1: PCA map of nations, coloured by archetype
    pca = PCA(n_components=2).fit(X)
    xy = pca.transform(X)
    fig, ax = plt.subplots(figsize=(10, 7))
    for c in range(K):
        m = km.labels_ == c
        ax.scatter(xy[m, 0], xy[m, 1], s=70, color=PALETTE[c], label=names[c],
                   edgecolor="white", linewidth=0.6, zorder=3)
    # label the notable nations (largest totals + a few specialists)
    show = set(mat.sort_values("total", ascending=False).index[:16]) | {"JAM", "KEN", "ETH", "NOR", "JPN", "CHN"}
    for i, nat in enumerate(mat.index):
        if nat in show:
            ax.annotate(nat, (xy[i, 0], xy[i, 1]), fontsize=8.5, color=INK,
                        xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%} of variance — overall depth)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%} — sprint/power ↔ distance)")
    ax.set_title("National athletics archetypes (WA points across five disciplines)",
                 fontweight="bold", fontsize=13)
    ax.legend(frameon=False, fontsize=9, loc="best")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "archetypes_map.png", dpi=150); plt.close(fig)

    # Fig 2: heatmap of the top nations' category z-scores, grouped by cluster
    top = mat.sort_values(["cluster", "total"], ascending=[True, False]).head(28)
    z = zmat.loc[top.index, CATS]
    fig, ax = plt.subplots(figsize=(8.5, 10))
    im = ax.imshow(z.values, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(len(CATS))); ax.set_xticklabels([c.capitalize() for c in CATS])
    ax.set_yticks(range(len(top))); ax.set_yticklabels(top.index, fontsize=8.5)
    for y, nat in enumerate(top.index):
        for x in range(len(CATS)):
            ax.text(x, y, f"{z.values[y, x]:+.1f}", ha="center", va="center", fontsize=6.5,
                    color="white" if abs(z.values[y, x]) > 1.1 else "#333")
    ax.set_title("Who's good at what\n(WA-point strength by discipline, z-scored)", fontweight="bold", fontsize=12)
    fig.colorbar(im, ax=ax, shrink=0.5, label="relative strength (z)")
    fig.tight_layout(); fig.savefig(FIG / "strength_heatmap.png", dpi=150); plt.close(fig)

    # Fig 3: archetype fingerprints (mean z-profile per cluster)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    width = 0.16
    for c in range(K):
        prof = zmat[zmat.cluster == c][CATS].mean()
        ax.bar(np.arange(len(CATS)) + (c - K/2) * width, prof.values, width,
               color=PALETTE[c], label=names[c])
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xticks(range(len(CATS))); ax.set_xticklabels([c.capitalize() for c in CATS])
    ax.set_ylabel("mean relative strength (z)")
    ax.set_title("Archetype fingerprints: what each cluster of nations is built on", fontweight="bold")
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(FIG / "archetype_fingerprints.png", dpi=150); plt.close(fig)
    print(f"\nwrote {len(list(FIG.glob('*.png')))} figures, {len(list(TAB.glob('*.csv')))} tables")


if __name__ == "__main__":
    main()
