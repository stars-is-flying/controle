import sys

def clear_terminal():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()