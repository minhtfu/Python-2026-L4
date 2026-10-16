import curses
from domains import MarkManager
from output import run_curses
from storage import load_data, compress_data


if __name__ == "__main__":
    manager = MarkManager()
    load_data(manager)

    try:
        run_curses(manager)
    except curses.error:
        print("curses UI is unavailable in this terminal.")

    compress_data()
