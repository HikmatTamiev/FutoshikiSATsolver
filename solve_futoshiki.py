import sys


def read_order(text):
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        return int(line)
    raise ValueError("The file does not contain an order.")


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    order = read_order(text)
    print("Futoshiki order", order)


if __name__ == "__main__":
    main()
