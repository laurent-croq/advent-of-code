import argparse, requests, sys, re, os, shutil, datetime, time, glob, json

assert sys.version_info >= (3, 8)

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

def run(puzzles, samples=None):
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
        puzzle_lines = [ args.line ]
    else:
        if args.input_file is None:
            if args.year is None or args.day is None:
                if sys.argv[0][0] == "/":
                    m = re.search(r'^.*\/(\d{4})\/day(\d{2})', os.path.normpath(sys.argv[0]))
                else:
                    m = re.search(r'^.*\/(\d{4})\/day(\d{2})', os.path.normpath(os.getcwd()+"/"+sys.argv[0]))
                year = datetime.datetime.now().year if m is None else int(m.group(1))
                day = datetime.datetime.now().day if m is None else int(m.group(2))

            if sys.argv[0][0] == "/":
                args.input_file = os.path.normpath("%s/inputs/day%02d" % (os.path.dirname(sys.argv[0]), day))
            else:
                args.input_file = os.path.normpath("%s/inputs/day%02d" % (os.path.dirname(os.getcwd()+"/"+sys.argv[0]), day))

            if args.sample:
                args.input_file += "."+args.sample
            else:
                fetch_puzzle_input(year, day, args.input_file, reload=args.reload)
                if samples is not None:
                    for sample in samples:
                        print("Checking sample %s:" % sample)
                        with open(args.input_file + "."+str(sample)) as f:
                            puzzle_lines = f.read().splitlines()
                        
                        answers = puzzles(puzzle_lines)
                        answer1 = next(answers)
                        if answer1 == samples[sample][0]:
                            print("- answer1 = %s [OK]" % answer1)
                        else:
                            print("- answer1 = %s [NOK] (expected %s)" % (answer1, samples[sample][0]))
                            sys.exit(1)

                        answer2 = next(answers)
                        if answer2 == samples[sample][1]:
                            print("- answer2 = %s [OK]" % answer2)
                        else:
                            print("- answer2 = %s [NOK] (expected %s)" % (answer2, samples[sample][1]))
                            sys.exit(1)

        print("Reading puzzle input from %s" % args.input_file)
        with open(args.input_file) as f:
            puzzle_lines = f.read().splitlines()

    answers = puzzles(puzzle_lines)
    print("answer1 = %s" % next(answers))
    print("answer2 = %s" % next(answers))
