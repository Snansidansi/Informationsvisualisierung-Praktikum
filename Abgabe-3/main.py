import sys

if __name__ == "__main__":
    try:
        csvPath = sys.argv[1]
    except Exception as e:
        print("Bitte den Dateipfad zu der csv als command line argument übergeben")
        exit(1)
