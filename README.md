# Layer Grid View

A QGIS plugin that displays visible project layers in a dockable panel arranged as a grid, enabling simultaneous comparison of multiple layers with automatic navigation synchronization.

## Overview

**Layer Grid View** was designed to facilitate comparative analysis of geospatial layers. When activated, the plugin presents a side panel containing a grid of mini-maps, each rendering a single layer independently. All pan and zoom interactions performed on the main QGIS map canvas are automatically replicated across every mini-map in the grid, ensuring consistent and synchronized visualization.

Coordinate reprojection is handled transparently: layers with different Coordinate Reference Systems (CRS) are automatically reprojected to the project CRS, eliminating the need for manual conversions.

## Features

- **Layer Grid** — Each visible layer is rendered in its own canvas, arranged in a 3-column grid within a dockable side panel.
- **Navigation Synchronization** — Pan and zoom operations on the main map canvas are automatically replicated across all grid canvases, maintaining spatial correspondence between views.
- **On-the-fly Reprojection** — Layers with different CRS are automatically reprojected to the project CRS, ensuring correct geographic overlay across all canvases.
- **Loading Indicator** — A "Loading..." overlay is displayed on each canvas during the rendering process, providing visual feedback to the user.
- **Message Logging** — Events, warnings, and errors are recorded in the QGIS Log Messages panel (`LayerGrid` tab), facilitating problem diagnosis.

## Requirements

| Component | Minimum Version |
|-----------|-----------------|
| QGIS      | 3.0             |

## Installation

Refer to the full installation and development environment setup guide in [INSTALLATION.md](INSTALLATION.md).

## Usage

### Project Setup

1. Add the layers you wish to compare to your QGIS project. Layers may have different Coordinate Reference Systems.
2. In the **Layers** panel, ensure the desired layers have their visibility checkbox enabled. Only visible layers will be included in the grid.

### Activating the Plugin

1. Navigate to `Plugins` → `Layer Grid View`.
2. A dockable panel will appear on the right side of the main window, displaying the canvas grid.

### Synchronized Navigation

1. Perform pan (drag) and zoom (scroll) operations on the main QGIS map canvas. All grid canvases will automatically follow the navigation, maintaining the same geographic extent.

### Event Monitoring

1. To view plugin log messages, navigate to `View` → `Panels` → `Log Messages` and select the **LayerGrid** tab.

## Known Limitations

- The grid is built at the time the plugin is opened. To reflect changes in the visible layer list (addition, removal, or visibility changes), the plugin must be closed and reopened.
- The grid layout uses a fixed number of 3 columns, with no customization option in the current version.

## License

This plugin is distributed under the terms of the [GNU General Public License v2.0](LICENSE) or later.
