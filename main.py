import sys
import argparse
from router import Router

# create_dataset
# "F:\projects\pony_pre_proj\all"
# "F:\projects\pony_pre_proj"
# tacatron_dataset
# Fluttershy
# "Clean"
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepares dataset for Deepvoice and tacatron")
    parser.add_argument('args', metavar='N', type=str, nargs='+', help='old-args-dependency, fix later')
    parser.add_argument('--skip_time', help="Minimum time of audio clip (in sec)", type=int, default=0)
    parsed = parser.parse_args()
    args = parsed.args
    args.append(parsed.skip_time)
    Router(args[0], *args[1:])
