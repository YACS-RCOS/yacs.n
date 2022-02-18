import requests
import sys

"""Script to determine if a website returns a 404 error."""


def main():

    for url in range(1, len(sys.argv)):
        URL = sys.argv[url]
        response = requests.get(URL)
        if response.status_code == 404:
            exit(1)
    exit(0)


if __name__ == "__main__":
    main()
    