import argparse, requests, sys, re, os, shutil, datetime

def fetch_puzzle_input(year, day, puzzle_input_filename, reload=False):
    if os.path.isfile(puzzle_input_filename) and not reload:
        return

    puzzle_input_url = "https://adventofcode.com/%d/day/%d/input" % (int(year), int(day))
    try:
        session_id = os.environ['AOC_SESSION_ID']
    except KeyError:
        print("AOC_SESSION_ID environment variable is not defined")
        sys.exit(1)

    print("Fetching puzzle input %s in %s" % (puzzle_input_url, puzzle_input_filename))
    with requests.get(puzzle_input_url, cookies={"session": session_id}, stream=True) as r:
        if r.status_code == 404:
            print("Got a 404 : puzzle not yet available or bad session_id ?")
            sys.exit(1)
        r.raise_for_status()
        r.raw.decode_content = True
        with open(puzzle_input_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def read_puzzle_input(year=datetime.datetime.now().year):
    parser = argparse.ArgumentParser()
    parser.add_argument("--line", "-l")
    parser.add_argument("--sample", "-s")
    parser.add_argument("--reload", "-r", action='store_true')
    parser.add_argument("input_file", nargs='?')
    args = parser.parse_args()

    if args.line is not None:
        print("Using string '%s' as puzzle input" % args.line)
        yield(args.line)
    else:
        if args.input_file is None:
            m = re.search('^.*\/day(\d{2})', sys.argv[0])
            if not m:
                print("Could not identify day from %s" % sys.argv[0])
                sys.exit(1)

            day = m.group(1)
            args.input_file = "inputs/day%s" % day

            if args.sample:
                args.input_file += "."+args.sample
            else:
                fetch_puzzle_input(year, day, args.input_file, reload=args.reload)

        print("Reading puzzle input from %s" % args.input_file)
        with open(args.input_file) as f:
            for line in f:
                yield(line.rstrip("\n"))

def load_puzzle_input(year=datetime.datetime.now().year):
    return([ line for line in read_puzzle_input(year) ])
