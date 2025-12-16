import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pipeline import run_pipeline

if __name__ == "__main__":
    for i in range(3):
        print(f"Run {i + 1}")
        run_pipeline()
