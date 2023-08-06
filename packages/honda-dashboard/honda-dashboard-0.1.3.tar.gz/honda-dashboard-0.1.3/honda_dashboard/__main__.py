import sys

from honda_dashboard.dashboard import Dashboard


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    app = Dashboard()
    app.run()


if __name__ == "__main__":
    main()
