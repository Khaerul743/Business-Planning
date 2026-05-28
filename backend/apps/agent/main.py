"""Main entry point to run the LangGraph development server."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Run the LangGraph development server."""
    # Get the directory containing this script
    project_dir = Path(__file__).parent / "src"
    
    # Run langgraph dev command
    try:
        result = subprocess.run(
            ["langgraph", "dev"],
            cwd=project_dir,
            check=True,
        )
        sys.exit(result.returncode)
    except FileNotFoundError:
        print(
            "Error: 'langgraph' command not found. "
            "Please install langgraph: pip install langgraph"
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: LangGraph development server failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
