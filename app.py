import sys
import os

# Add the 'app' module to the path so it can find it
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.main import main

if __name__ == "__main__":
    main()
