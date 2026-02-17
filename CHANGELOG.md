# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-17

### Added

- **On-the-fly CRS reprojection**: layers with different Coordinate Reference
  Systems are automatically reprojected to the project CRS for consistent
  display across all grid canvases.
- **Project CRS change listener**: grid canvases update automatically when
  the project CRS is changed (`crsChanged` signal).
- **CRS transform cache**: coordinate transforms are cached to avoid
  redundant object creation during pan/zoom synchronization.
- **Debounced zoom sync**: extent synchronization uses a 50 ms `QTimer`
  debounce to batch rapid pan/zoom events and reduce flickering.
- **No-selection dialog**: when no layers are selected, a detailed
  instructional dialog guides the user on how to select layers.
- **INSTALLATION.md**: dedicated installation and development guide.
- **CHANGELOG.md**: this file.
- **Makefile targets**: `help` (default), `validate`, `publish`, with
  symlink detection in `deploy`.
- **Test data generator**: script to create polygon layers across 8 different
  CRS for reprojection validation (`tests/create_test_layers.py`).

### Changed

- **Layer selection model**: the plugin now uses **selected** layers
  (highlighted in the Layers panel) instead of all visible (checked) layers.
- **README.md**: rewritten in English with formal tone, detailed feature
  descriptions, and structured usage instructions.
- **LICENSE**: updated from MIT to GNU General Public License v2.0+,
  aligning with plugin headers and `metadata.txt`.
- **Makefile**: modernized with `pytest` (replacing `nosetests`), absolute
  deploy path, and proper `clean` target (`__pycache__`, `.pyc`,
  `.pytest_cache`).
- **pb_tool.cfg**: added `canvas.py` to `python_files`.
- **canvas.py**: fixed import from `PyQt5.QtWidgets` to `qgis.PyQt.QtWidgets`
  for cross-platform compatibility.

### Removed

- **Slider dead code**: removed `QSlider` import, `self.slider`,
  `self.layer_ids`, `self.current_layer_id`, and the entire
  `updateLayerVisibility()` method.
- **Hardcoded EPSG:4326**: removed `setDestinationCrs(EPSG:4326)` on the
  main canvas, which was destructively overriding the user's project CRS.
- **Redundant calls**: removed `canvas.repaint()` (redundant after
  `refresh()`) and `canvas.showLoading()` from zoom sync (caused flicker).

### Fixed

- **Mutable default argument**: `get_checked_nodes(visible_layers=[])` changed
  to `visible_layers=None` pattern.
- **Signal lifecycle**: `extentsChanged` and `crsChanged` signals are now
  properly disconnected in `onClosePlugin()`.
- **Widget cleanup**: replaced `widget.setParent(None)` with
  `widget.deleteLater()` for proper Qt object lifecycle.
- **Logging**: replaced all `print()` calls with `QgsMessageLog.logMessage()`
  for proper QGIS log integration.
- **`self.iface = None` in close**: removed the assignment that was breaking
  `unload()` after closing the dock widget.

## [1.0.0] - 2023-09-23

### Added

- Initial release.
- Dockable grid widget displaying visible layers in a 3-column layout.
- Pan/zoom synchronization between main canvas and grid canvases.
- Loading indicator overlay on each canvas.
- Error handling via QGIS message bar.
