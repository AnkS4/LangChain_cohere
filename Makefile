# Default target (run when you type 'make')
.PHONY: help list install run clean

# Configuration
SRC_DIR = src

help:
	@echo "Available commands:"
	@echo "  make install    # Install dependencies"
	@echo "  make list       # List all Python programs"
	@echo "  make run SCRIPT=filename  # Run a Python program (default: l1.py)"
	@echo "  make clean      # Clean up"
	@echo "  make help       # Show this help"

# List all Python programs
list:
	@echo "Available Python programs:"
	@ls -1 $(SRC_DIR)/*.py 2>/dev/null | sed 's|^$(SRC_DIR)/||' || echo "No Python files found"

# Install dependencies
install:
	# uv init
	uv sync

# Run a Python program
run:
	@if [ -z "$(SCRIPT)" ]; then \
		SCRIPT="$(SRC_DIR)/l1.py"; \
	else \
		SCRIPT="$(SRC_DIR)/$$(echo "$(SCRIPT)" | sed 's|^$(SRC_DIR)/||')"; \
	fi; \
	if [ ! -f "$$SCRIPT" ]; then \
		echo "Error: '$$(basename "$$SCRIPT")' not found. Available Python programs:"; \
		ls -1 $(SRC_DIR)/*.py 2>/dev/null | sed 's|^$(SRC_DIR)/||' || echo "No Python files found"; \
		exit 1; \
	fi; \
	echo "Running $$(basename "$$SCRIPT")..."; \
	uv run "$$SCRIPT"

# Clean up
clean:
	rm -rf .venv __pycache__ .coverage
	find . -type d \( -name "*.egg-info" -o -name "__pycache__" \) -exec rm -rf {} +
