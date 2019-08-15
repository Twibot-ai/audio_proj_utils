import sys
from router import Router

if __name__ == "__main__":
    args = sys.argv
    Router(args[1], *args[2:])
