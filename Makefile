#/***************************************************************************
# LayerGridView
#
# The Layer Grid Plugin provides an intuitive dockable widget that presents
# a grid of map canvases.
#                            -------------------
#       begin               : 2023-09-23
#       copyright           : (C) 2023 by Tharles de Sousa Andrade
#       email               : irtharles@gmail.com
# ***************************************************************************/
#
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

PLUGINNAME = layer_grid_view

PY_FILES = \
	__init__.py \
	layer_grid_view.py \
	layer_grid_view_dockwidget.py \
	canvas.py

UI_FILES = layer_grid_view_dockwidget_base.ui

EXTRAS = metadata.txt icon.png

COMPILED_RESOURCE_FILES = resources.py

DEPLOY_DIR = $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins/$(PLUGINNAME)

REQUIRED_FILES = __init__.py metadata.txt icon.png resources.py
REQUIRED_META = name version qgisMinimumVersion description author email tracker repository

.PHONY: help deploy test validate publish clean pylint

help:
	@echo ""
	@echo "  deploy   - Deploy plugin to local QGIS plugins directory"
	@echo "  test     - Run tests with pytest"
	@echo "  validate - Validate plugin structure for OSGEO"
	@echo "  publish  - Create ZIP for plugins.qgis.org"
	@echo "  clean    - Remove generated files"
	@echo "  pylint   - Run linter"
	@echo ""

compile: $(COMPILED_RESOURCE_FILES)

%.py : %.qrc
	pyrcc5 -o $*.py $<

deploy: compile
	@if [ -L "$(DEPLOY_DIR)" ]; then \
		echo "Symlink detected: $(DEPLOY_DIR) -> $$(readlink -f $(DEPLOY_DIR))"; \
		echo "No copy needed. Plugin is already linked."; \
	else \
		echo "Deploying plugin to $(DEPLOY_DIR)"; \
		mkdir -p $(DEPLOY_DIR); \
		cp -vf $(PY_FILES) $(DEPLOY_DIR)/; \
		cp -vf $(UI_FILES) $(DEPLOY_DIR)/; \
		cp -vf $(COMPILED_RESOURCE_FILES) $(DEPLOY_DIR)/; \
		cp -vf $(EXTRAS) $(DEPLOY_DIR)/; \
		if [ -d i18n ]; then cp -vfr i18n $(DEPLOY_DIR)/; fi; \
		echo "Deploy complete."; \
	fi

test: compile
	@echo ""
	@echo "----------------------"
	@echo "Running tests"
	@echo "----------------------"
	@export PYTHONPATH=$$(pwd):$(PYTHONPATH); \
		export QGIS_DEBUG=0; \
		export QGIS_LOG_FILE=/dev/null; \
		python -m pytest -v tests/ || true
	@echo "----------------------"

validate:
	@echo "Validating plugin structure..."
	@ERRORS=0; \
	for f in $(REQUIRED_FILES); do \
		if [ ! -f "$$f" ]; then \
			echo "  MISSING: $$f"; \
			ERRORS=$$((ERRORS + 1)); \
		fi; \
	done; \
	for key in $(REQUIRED_META); do \
		if ! grep -q "^$$key=" metadata.txt 2>/dev/null; then \
			echo "  MISSING metadata key: $$key"; \
			ERRORS=$$((ERRORS + 1)); \
		fi; \
	done; \
	VERSION=$$(grep "^version=" metadata.txt | cut -d= -f2); \
	if ! echo "$$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$$'; then \
		echo "  INVALID version format: $$VERSION (expected X.Y.Z)"; \
		ERRORS=$$((ERRORS + 1)); \
	fi; \
	TRACKER=$$(grep "^tracker=" metadata.txt | cut -d= -f2); \
	REPO=$$(grep "^repository=" metadata.txt | cut -d= -f2); \
	for url in "$$TRACKER" "$$REPO"; do \
		if ! echo "$$url" | grep -qE '^https?://'; then \
			echo "  INVALID URL: $$url"; \
			ERRORS=$$((ERRORS + 1)); \
		fi; \
	done; \
	if [ $$ERRORS -eq 0 ]; then \
		echo "  All checks passed."; \
	else \
		echo "  $$ERRORS error(s) found."; \
		exit 1; \
	fi

publish: compile validate
	@echo "Creating plugin ZIP..."
	rm -f $(PLUGINNAME).zip
	mkdir -p /tmp/$(PLUGINNAME)
	cp $(PY_FILES) $(UI_FILES) $(COMPILED_RESOURCE_FILES) $(EXTRAS) /tmp/$(PLUGINNAME)/
	@if [ -d i18n ]; then cp -r i18n /tmp/$(PLUGINNAME)/; fi
	cd /tmp && zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME) \
		-x "$(PLUGINNAME)/__pycache__/*" \
		-x "$(PLUGINNAME)/*.pyc" \
		-x "$(PLUGINNAME)/.git/*"
	rm -rf /tmp/$(PLUGINNAME)
	@SIZE=$$(stat -c%s $(PLUGINNAME).zip 2>/dev/null || stat -f%z $(PLUGINNAME).zip); \
	MAX=$$((20 * 1024 * 1024)); \
	if [ $$SIZE -gt $$MAX ]; then \
		echo "ERROR: ZIP exceeds 20MB ($$SIZE bytes)"; \
		rm -f $(PLUGINNAME).zip; \
		exit 1; \
	fi; \
	echo "Created $(PLUGINNAME).zip ($$SIZE bytes)"

clean:
	@echo "Cleaning generated files..."
	rm -f $(PLUGINNAME).zip
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache
	@echo "Clean complete."

pylint:
	@echo ""
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --reports=n --rcfile=pylintrc $(PY_FILES) || true
