"""
Rendering of an abstract plot to a concrete format.
"""
from typing import Callable, List

from .abstract import AbstractColumn, AbstractPlot
from .istyle import iStyle


def render(plot: AbstractPlot, styler: Callable[..., iStyle]) -> str:
    """
    Render the plot as an SVG using the specified style.

    Args:
        plot: The abstract plot to render
        styler: The style to use in the rendering. For example `dagviz.style.metro.svg_renderer`
    Returns:
        A string with the SVG content.
    """
    # Initialize the style using the provided styler function
    style: iStyle = styler(plot.colors, -plot.columns.start)

    # Iterate over each row in the plot
    for row in plot.rows:
        last_col = 0
        arcs: List[AbstractColumn] = []
        nodepos = (0, 0)
        node_pos = 1

        # Iterate over each column in the row
        for col in row:
            last_col = col.column
            curpos = (col.column, row.row)

            # If the column is a node, place the node and handle arcs
            if col.is_node:
                nodepos = curpos
                style.place_node(curpos, col.color, row.label)
                if len(arcs) != 0:
                    style.place_left_hline(
                        (arcs[0].column, row.row), curpos, arcs[0].color
                    )
                    arcs = []
                arcs.append(col)
                node_pos = 0

            # If the column is an input, place arcs and vertical lines
            if col.is_input:
                if node_pos < 0:
                    arcs.append(col)
                    style.place_left_arc(curpos, col.color)
                    if col.is_last:
                        style.place_vline_arc(
                            (col.column, col.start_row.row),
                            curpos,
                            col.start_row.columns[col.column].color,
                        )
                elif node_pos == 0:
                    style.place_vline_node(
                        (col.column, col.start_row.row),
                        curpos,
                        col.start_row.columns[col.column].color,
                    )
                else:
                    arcs.append(col)
                    style.place_right_arc(curpos, col.color)
                    if col.is_last:
                        style.place_vline_arc(
                            (col.column, col.start_row.row),
                            curpos,
                            col.start_row.columns[col.column].color,
                        )

            # Update node position
            if col.is_node:
                node_pos = -1

        # Place horizontal line if there are multiple arcs
        if len(arcs) >= 2:
            style.place_right_hline(
                (arcs[0].column, row.row), (arcs[-1].column, row.row), arcs[-1].color
            )

        # Place the label for the row
        style.place_label(nodepos, (last_col + 1, row.row), row.label)

    # Return the SVG content as a string
    return style.dumps()
