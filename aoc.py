import argparse, requests, sys, re, os, shutil, datetime, time, glob, json

def fetch_puzzle_input(year, day, puzzle_input_filename, reload=False):
    if os.path.isfile(puzzle_input_filename) and not reload:
        return

    try:
        session_id = os.environ['AOC_SESSION_ID']
    except KeyError:
        print("AOC_SESSION_ID environment variable is not defined")
        sys.exit(1)

    puzzle_input_url = "https://adventofcode.com/%d/day/%d/input" % (year, day)
    print("Fetching puzzle input %s and saving in %s" % (puzzle_input_url, puzzle_input_filename))
    with requests.get(puzzle_input_url, cookies={"session": session_id}, stream=True) as r:
        if r.status_code == 404:
            print("Got a 404 : puzzle not yet available or bad session_id ?")
            sys.exit(1)
        r.raise_for_status()
        r.raw.decode_content = True
        with open(puzzle_input_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def read_puzzle_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--line", "-l")
    parser.add_argument("--sample", "-s")
    parser.add_argument("--day", "-d", type=int)
    parser.add_argument("--year", "-y", type=int)
    parser.add_argument("--reload", "-r", action='store_true')
    parser.add_argument("input_file", nargs='?')
    args = parser.parse_args()

    if args.line is not None:
        print("Using string '%s' as puzzle input" % args.line)
        yield(args.line)
    else:
        if args.input_file is None:
            if args.year is None or args.day is None:
                m = re.search(r'^.*\/(\d{4})\/day(\d{2})', os.path.normpath(os.getcwd()+"/"+sys.argv[0]))
                if m is not None:
                    year = int(m.group(1))
                    day = int(m.group(2))
                else:
                    year = datetime.datetime.now().year
                    day = datetime.datetime.now().day

            args.input_file = "inputs/day%02d" % day

            if args.sample:
                args.input_file += "."+args.sample
            else:
                fetch_puzzle_input(year, day, args.input_file, reload=args.reload)

        print("Reading puzzle input from %s" % args.input_file)
        with open(args.input_file) as f:
            for line in f:
                yield(line.rstrip("\n"))

def load_puzzle_input():
    return([ line for line in read_puzzle_input() ])
