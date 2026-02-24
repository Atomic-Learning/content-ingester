import json
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
INPUTS_DIR = Path(__file__).parent.parent / "inputs"
GRAPH_PATH = OUTPUTS_DIR / "prerequisite_graph.png"

NEW_COLOR = "#b6e7a7"  # light green
EXISTING_COLOR = "#cccccc"  # light gray
FONT_COLOR = "red"


def get_existing_slugs():
    current_content = INPUTS_DIR / "current_content.md"
    slugs = set()
    if not current_content.exists():
        return slugs
    with open(current_content, encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("- slug: "):
                slug = line.strip().split(":", 1)[1].strip()
                slugs.add(slug)
    return slugs


def get_new_pages():
    pages = {}
    for page_dir in OUTPUTS_DIR.iterdir():
        if not page_dir.is_dir():
            continue
        meta = page_dir / "metadata.json"
        if not meta.exists():
            continue
        with open(meta, encoding="utf-8") as f:
            data = json.load(f)
        slug = data.get("slug")
        prereqs = data.get("prerequisites", [])
        if slug:
            pages[slug] = prereqs
    return pages


def main():
    new_pages = get_new_pages()
    all_slugs = set(new_pages.keys())
    G = nx.DiGraph()
    # Add nodes
    for slug in new_pages:
        G.add_node(slug, color=NEW_COLOR)
    for slug in set(pr for prereqs in new_pages.values() for pr in prereqs):
        if slug not in all_slugs:
            G.add_node(slug, color=EXISTING_COLOR)
    # Add edges
    for slug, prereqs in new_pages.items():
        for pr in prereqs:
            G.add_edge(pr, slug)
    num_nodes = len(G.nodes)
    # Layout: use graphviz_layout if possible, else spring_layout with k
    try:
        from networkx.drawing.nx_pydot import graphviz_layout
        pos = graphviz_layout(G, prog="dot")
    except Exception:
        k = 6 / (num_nodes ** 0.5) if num_nodes > 1 else 1
        pos = nx.spring_layout(G, seed=42, k=k)
    # Scaling: as node count increases, decrease node/font/arrow size
    base_node_size = 2500
    base_font_size = 12
    base_arrow_size = 25
    scale = max(0.5, min(1.5, 30 / num_nodes)) if num_nodes > 0 else 1
    node_size = base_node_size * scale
    font_size = int(base_font_size * scale)
    arrow_size = int(base_arrow_size * scale)
    node_colors = [G.nodes[n].get('color', '#cccccc') for n in G.nodes]
    plt.figure(figsize=(24, 16))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        edge_color="#333333",
        font_size=font_size,
        font_weight="bold",
        arrows=True,
        arrowsize=arrow_size,
        linewidths=2,
        width=2,
        node_size=node_size,
        connectionstyle='arc3,rad=0.1',
        labels={n: n for n in G.nodes},
        font_color=FONT_COLOR
    )
    plt.title("Prerequisite Graph (Green: New, Gray: Existing)", fontsize=18)
    plt.tight_layout()
    plt.savefig(GRAPH_PATH)
    plt.close()
    print(f"Graph generated at {GRAPH_PATH}")

if __name__ == "__main__":
    main()
