import curses
from domains import MarkManager
from output import run_curses


if __name__ == "__main__":
    manager = MarkManager()
    try:
        run_curses(manager)
    except curses.error:
        print("curses UI is unavailable in this terminal.")
