#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = PianoTrainer
PYTHON_INTERPRETER = python
MAIN_SCRIPT = ./piano_chords/main.py
DIST_DIR = dist
ICON_FILE = piano_chords/logo/icon.icns

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Run the app
.PHONY: run
run:
	uv run $(MAIN_SCRIPT)

## Run tests
.PHONY: test
test:
	uv run pytest test_chords.py -v

## Build the app with PyInstaller (macOS GUI)
.PHONY: build
build:
	uv run pyinstaller \
		--windowed \
		--onefile \
		--name $(PROJECT_NAME) \
		--icon=$(ICON_FILE) \
		--collect-submodules piano_chords.pages \
		--collect-submodules mido.backends \
		$(MAIN_SCRIPT)

## Zip the .app for distribution
.PHONY: zip
zip:
	cd $(DIST_DIR) && zip -r $(PROJECT_NAME).zip $(PROJECT_NAME).app
	@echo ">>> Zip created at $(DIST_DIR)/$(PROJECT_NAME).zip"

## Clean up build artifacts
.PHONY: clean
clean:
	rm -rf build
	rm -rf $(DIST_DIR)
	rm -rf *.spec
	find . -type d -name "__pycache__" -exec rm -rf {} +
