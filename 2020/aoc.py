import argparse, requests, sys, re, os, shutil, datetime, time, glob, json

def fetch_puzzle_input(year, day, reload=False):
    try:
        puzzle_input_filename = "inputs/day%02d" % int(day)
    except:
        print("Bad day specifier: %s" % day)
        sys.exit(1)

    if os.path.isfile(puzzle_input_filename) and not reload:
        return(puzzle_input_filename)

    puzzle_input_url = "https://adventofcode.com/%d/day/%d/input" % (int(year), int(day))
    try:
        session_id = os.environ['AOC_SESSION_ID']
    except KeyError:
        print("AOC_SESSION_ID environment variable is not defined")
        sys.exit(1)

    print("Fetching puzzle input %s and saving in %s" % (puzzle_input_url, puzzle_input_filename))
    with requests.get(puzzle_input_url, cookies={"session": session_id}, stream=True) as r:
        if r.status_code == 404:
            print("Got a 404 : puzzle not yet available or bad session_id ?")
            sys.exit(1)
        r.raise_for_status()
        r.raw.decode_content = True
        with open(puzzle_input_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return(puzzle_input_filename)

def read_puzzle_input(year=datetime.datetime.now().year):
    parser = argparse.ArgumentParser()
    parser.add_argument("--string", "-s")
    parser.add_argument("--reload", "-r", action='store_true')
    parser.add_argument("input_file", nargs='?')
    args = parser.parse_args()

    if args.string is not None:
        yield(args.string)
    else:
        if args.input_file is None:
            m = re.search(r'^.*\/day(\d{2})', sys.argv[0])
            if not m:
                print("Could not identify day from %s" % sys.argv[0])
                sys.exit(1)
            args.input_file = fetch_puzzle_input(year, m.group(1), reload=args.reload)

        with open(args.input_file) as f:
            for line in f:
                yield(line.rstrip("\n"))

def load_puzzle_input(year=datetime.datetime.now().year):
    return([ line for line in read_puzzle_input(year) ])
