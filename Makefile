#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = piano_chords
PYTHON_INTERPRETER = python
MAIN_SCRIPT = ./piano_chords/main.py
DIST_DIR = dist
DIST_NAME = PianoTrainer

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Run the app
.PHONY: run
run:
	uv run $(MAIN_SCRIPT)

## Build the app with PyInstaller (macOS GUI)
.PHONY: build
build:
	uv run pyinstaller \
		--windowed \
		--onefile \
		--name $(DIST_NAME) \
		--icon=piano_chords/logo/icon.icns \
		--collect-submodules piano_chords.pages \
		--collect-submodules mido.backends \
		$(MAIN_SCRIPT)

## Clean up build artifacts
.PHONY: clean
clean:
	rm -rf build
	rm -rf $(DIST_DIR)
	rm -rf *.spec
	find . -type d -name "__pycache__" -exec rm -rf {} +

