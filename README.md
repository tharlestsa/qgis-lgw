# Layer Grid Plugin for QGIS

## Description

The Layer Grid Plugin provides an intuitive dockable widget that presents a grid of map canvases, showcasing each layer sorted by a custom property, "date". This allows users to easily compare different layers side by side. Moreover, zooming or panning in the main map canvas will automatically sync the zoom and pan actions in the grid canvases, ensuring consistent visualization across all maps.

## Features

- **Synced View**: Automatically sync zoom and pan actions across main map and grid canvases.
- **Grid Layout**: Clear, intuitive grid layout to view layers side by side.
- **Error Handling**: Displays error messages through QGIS's message bar in case of issues.

## Installation

1. Download the Layer Grid Plugin `.zip` file.
2. Open QGIS.
3. Navigate to `Plugins` > `Manage and Install Plugins...` > `Install from ZIP`.
4. Select the downloaded `.zip` file and click 'Install Plugin'.
5. Once installed, the Layer Grid widget should be available in the QGIS interface.

## Usage

1. Open the Layer Grid dockable widget by navigating to `Plugins`  > `Layer Grid`.
2. The layers you have in your project will be automatically displayed in the grid, sorted by their custom "date" property.
3. Interact with the main QGIS map canvas (pan, zoom). Notice that the map canvases in the grid will automatically adjust to match the main canvas's current view.

## Contributions & Feedback

We welcome contributions and feedback on the plugin. If you have suggestions or find any bugs, please report them to our [GitHub repository](#).

## License

This plugin is licensed under the MIT License. Refer to the `LICENSE` file for more details.
