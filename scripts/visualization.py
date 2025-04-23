import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

try:
    from pyvis.network import Network

    HAS_PYVIS = True
except ImportError:
    HAS_PYVIS = False

CORRELATED_PATH = Path(__file__).parents[1] / "data/correlated_results.json"
VISUAL_OUT_DIR = Path(__file__).parents[1] / "data/visualizations"
VISUAL_OUT_DIR.mkdir(exist_ok=True)


def visualize_correlations():
    # Build the graph
    G = nx.Graph()

    # Load correlation results
    try:
        with open(CORRELATED_PATH, "r") as f:
            data = json.load(f)
            print("Loaded correlation data.")
    except Exception as e:
        print(f"Failed to load correlation file: {e}")
        return

    # Add phone correlations
    for phone, files in data.get("phones", {}).items():
        G.add_node(phone, type="phone")
        for f in files:
            G.add_node(f, type="file")
            G.add_edge(phone, f)

    # Add breach correlations
    for breach, files in data.get("breaches", {}).items():
        G.add_node(breach, type="breach")
        for f in files:
            G.add_node(f, type="file")
            G.add_edge(breach, f)

    # Add username correlations
    for site, files in data.get("usernames", {}).items():
        G.add_node(site, type="username")
        for f in files:
            G.add_node(f, type="file")
            G.add_edge(site, f)

    # Add domain correlations
    for domain, files in data.get("domains", {}).items():
        G.add_node(domain, type="domain")
        for f in files:
            G.add_node(f, type="file")
            G.add_edge(domain, f)

    # Add IP correlations
    for ip, files in data.get("ips", {}).items():
        G.add_node(ip, type="ip")
        for f in files:
            G.add_node(f, type="file")
            G.add_edge(ip, f)

    # Fallback if nothing found
    if G.number_of_nodes() == 0:
        print("No correlations found — displaying placeholder node.")
        G.add_node("No Correlations Found", type="info")
        node_colors = ["lightgray"]
    else:
        node_colors = []
        for _, attrs in G.nodes(data=True):
            node_type = attrs.get("type")
            if node_type == "phone":
                node_colors.append("skyblue")
            elif node_type == "breach":
                node_colors.append("lightcoral")
            elif node_type == "username":
                node_colors.append("mediumpurple")
            elif node_type == "domain":
                node_colors.append("gold")
            elif node_type == "ip":
                node_colors.append("lightsteelblue")
            elif node_type == "file":
                node_colors.append("lightgreen")
            else:
                node_colors.append("lightgray")

    # Draw static PNG
    plt.figure(figsize=(16, 12), constrained_layout=True)
    nx.draw(
        G,
        with_labels=True,
        node_color=node_colors,
        node_size=1200,
        font_size=9,
        font_weight="bold",
        edge_color="gray",
    )
    plt.title("Auton-OSINT Correlation Graph")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_path = VISUAL_OUT_DIR / f"correlation_graph_{timestamp}.png"
    plt.savefig(img_path, dpi=300)
    print(f"Graph saved to {img_path}")
    plt.show()

    # Draw interactive HTML (if pyvis is available)
    if HAS_PYVIS:
        net = Network(height="100%", width="100%")
        for node, attrs in G.nodes(data=True):
            net.add_node(
                node,
                label=node,
                title=node,
                group=attrs.get("type"),
                value=nx.degree(G, node),
            )
        for u, v in G.edges():
            net.add_edge(u, v)
        html_path = VISUAL_OUT_DIR / f"correlation_graph_{timestamp}.html"
        net.show(html_path)
        print(f"Interactive graph saved to {html_path}")
    else:
        print("pyvis not installed; skipping interactive HTML export")


if __name__ == "__main__":
    visualize_correlations()
