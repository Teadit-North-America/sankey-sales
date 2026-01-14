from pathlib import Path

import plotly.graph_objects as go


# =============================================================================
# OUTPUT CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path("output")
OUTPUT_FORMAT = "both"  # Options: "html", "png", "both"
OUTPUT_NAME = "sankey_chart"

# =============================================================================
# DATA - Edit this section to update values
# =============================================================================

# Product revenue (left side)
PRODUCTS = {
    "iPhone": 47.0,
    "Mac": 9.2,
    "iPad": 6.7,
    "Wearables": 9.377,
}

# Financial breakdown (will be calculated/assigned)
REVENUE = sum(PRODUCTS.values())  # 72.277

# Cost structure (right side of revenue)
COGS = 44.379
GROSS_PROFIT = 27.898

# Gross profit breakdown
OPERATING_EXPENSES = 20.199
OPERATING_PROFIT = 7.699

# Operating profit breakdown
NET_PROFIT = 5.638
TAXES = 2.118
OTHER = 0.056

# Operating expenses breakdown
INDUSTRIAL = 6.277
COMMERCIAL = 8.038
ADMINISTRATIVE = 4.069
R_AND_D = 0.010
HEADQTR = 0.936
DEPRECIATION = 0.868

# COGS breakdown
RAW_MATERIAL = 37.024
LABOR_COSTS = 5.365
OTHER_COGS = 1.990


# =============================================================================
# CHART CONFIGURATION
# =============================================================================

# Color palette - simplified (one color per category)
COLORS = {
    "blue": "#4A90D9",   # Products & Revenue
    "green": "#27AE60",  # Profit
    "red": "#C0392B",    # Costs & Expenses
}


def build_sankey_data():
    """Build the nodes and links for the Sankey diagram."""

    # Define all nodes with their values (order matters - index based)
    node_data = [
        # 0-3: Products (left)
        ("iPhone", PRODUCTS["iPhone"]),
        ("Mac", PRODUCTS["Mac"]),
        ("iPad", PRODUCTS["iPad"]),
        ("Wearables", PRODUCTS["Wearables"]),
        # 4: Revenue (center)
        ("Revenue", REVENUE),
        # 5-6: Revenue split
        ("Gross Profit", GROSS_PROFIT),
        ("COGS", COGS),
        # 7-8: Gross profit breakdown
        ("Operating Profit", OPERATING_PROFIT),
        ("Operating Expenses", OPERATING_EXPENSES),
        # 9-11: Operating profit breakdown
        ("Net Profit", NET_PROFIT),
        ("Taxes", TAXES),
        ("Other", OTHER),
        # 12-17: Operating expenses breakdown
        ("Industrial", INDUSTRIAL),
        ("Commercial", COMMERCIAL),
        ("Administrative", ADMINISTRATIVE),
        ("R & D", R_AND_D),
        ("Headqtr.", HEADQTR),
        ("Depreciation", DEPRECIATION),
        # 18-20: COGS breakdown
        ("Raw Material", RAW_MATERIAL),
        ("Labor Costs", LABOR_COSTS),
        ("Other Costs", OTHER_COGS),
    ]

    # Create labels with values (bold)
    labels = [f"<b>{name}</b><br><b>${value:.2f}M</b>" for name, value in node_data]

    # Node colors (by category)
    node_colors = [
        COLORS["blue"],   # iPhone
        COLORS["blue"],   # Mac
        COLORS["blue"],   # iPad
        COLORS["blue"],   # Wearables
        COLORS["blue"],   # Revenue
        COLORS["green"],  # Gross Profit
        COLORS["red"],    # COGS
        COLORS["green"],  # Operating Profit
        COLORS["red"],    # Operating Expenses
        COLORS["green"],  # Net Profit
        COLORS["red"],    # Taxes
        COLORS["green"],  # Other
        COLORS["red"],    # Industrial
        COLORS["red"],    # Commercial
        COLORS["red"],    # Administrative
        COLORS["red"],    # R & D
        COLORS["red"],    # Headqtr.
        COLORS["red"],    # Depreciation
        COLORS["red"],    # Raw Material
        COLORS["red"],    # Labor Costs
        COLORS["red"],    # Other Costs
    ]

    # Define links: (source_idx, target_idx, value)
    links = [
        # Products → Revenue
        (0, 4, PRODUCTS["iPhone"]),
        (1, 4, PRODUCTS["Mac"]),
        (2, 4, PRODUCTS["iPad"]),
        (3, 4, PRODUCTS["Wearables"]),
        # Revenue → Gross Profit / COGS
        (4, 5, GROSS_PROFIT),
        (4, 6, COGS),
        # Gross Profit → Operating Profit / Operating Expenses
        (5, 7, OPERATING_PROFIT),
        (5, 8, OPERATING_EXPENSES),
        # Operating Profit → Net Profit / Taxes / Other
        (7, 9, NET_PROFIT),
        (7, 10, TAXES),
        (7, 11, OTHER),
        # Operating Expenses → breakdown
        (8, 12, INDUSTRIAL),
        (8, 13, COMMERCIAL),
        (8, 14, ADMINISTRATIVE),
        (8, 15, R_AND_D),
        (8, 16, HEADQTR),
        (8, 17, DEPRECIATION),
        # COGS → breakdown
        (6, 18, RAW_MATERIAL),
        (6, 19, LABOR_COSTS),
        (6, 20, OTHER_COGS),
    ]

    # Unpack links
    sources = [l[0] for l in links]
    targets = [l[1] for l in links]
    values = [l[2] for l in links]

    # Link colors (semi-transparent, based on TARGET node)
    link_colors = [hex_to_rgba(node_colors[t], 0.5) for t in targets]

    return {
        "labels": labels,
        "node_colors": node_colors,
        "sources": sources,
        "targets": targets,
        "values": values,
        "link_colors": link_colors,
    }


def hex_to_rgba(hex_color, alpha):
    """Convert hex color to rgba string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def create_sankey_chart():
    """Create and return the Sankey figure."""

    data = build_sankey_data()

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=40,
                    thickness=40,
                    line=dict(width=0),
                    label=data["labels"],
                    color=data["node_colors"],
                    hovertemplate="%{label}<extra></extra>",
                ),
                link=dict(
                    source=data["sources"],
                    target=data["targets"],
                    value=data["values"],
                    color=data["link_colors"],
                    hovertemplate="%{source.label} → %{target.label}<br>$%{value:.2f}M<extra></extra>",
                ),
            )
        ]
    )

    fig.update_layout(
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="black",
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=900,
        width=1600,
        margin=dict(l=80, r=80, t=40, b=40),
    )

    return fig


def main():
    fig = create_sankey_chart()

    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Export based on format setting
    if OUTPUT_FORMAT in ("html", "both"):
        html_path = OUTPUT_DIR / f"{OUTPUT_NAME}.html"
        fig.write_html(html_path)
        print(f"Saved: {html_path}")

    if OUTPUT_FORMAT in ("png", "both"):
        png_path = OUTPUT_DIR / f"{OUTPUT_NAME}.png"
        fig.write_image(png_path, scale=2)
        print(f"Saved: {png_path}")

    # Show interactive chart in browser
    fig.show()


if __name__ == "__main__":
    main()
