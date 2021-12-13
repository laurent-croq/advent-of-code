import argparse, requests, sys, re, os, shutil, datetime, time, glob, json, copy

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
            print("Got 404 : puzzle not yet available or bad session_id ?")
            sys.exit(1)
        r.raise_for_status()
        r.raw.decode_content = True
        with open(puzzle_input_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

# Initialize extra arguments

def initialize_extra_args(args, sample=None, skip1=None, skip2=None):
    extra_args = dict(a.split("=") for a in (a for a in args.extra)) if args.extra is not None else {}
    extra_args['sample'] = (args.sample is not None) if sample is None else sample
    extra_args['skip1'] = args.skip1 if skip1 is None else skip1
    extra_args['skip2'] = args.skip2 if skip2 is None else skip2
    return(extra_args)

# Check expected answers for a set of samples

def check_samples(solve_puzzle, samples, args):
    for sample_id, sample_answers in samples.items():
        print("Checking sample %s:" % sample_id)
        with open(args.input_file + "."+str(sample_id)) as f:
            puzzle_lines = f.read().splitlines()
        
        # Determine extra arguments
        extra_args = initialize_extra_args(args, True, sample_answers[0] is None, sample_answers[1] is None)

        answers = solve_puzzle(puzzle_lines, **extra_args)
        answer1 = next(answers)
        if answer1 == sample_answers[0]:
            print("- answer1 = %s [OK]" % answer1)
        else:
            print("- answer1 = %s [FAIL] (expected %s)" % (answer1, sample_answers[0]))
            if not args.continue_on_error:
                sys.exit(1)

        answer2 = next(answers)
        if answer2 == sample_answers[1]:
            print("- answer2 = %s [OK]" % answer2)
        else:
            print("- answer2 = %s [FAIL] (expected %s)" % (answer2, sample_answers[1]))
            if not args.continue_on_error:
                sys.exit(1)
        print("")

def run(solve_puzzle, samples=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--line", "-l")
    parser.add_argument("--sample", "-s")
    parser.add_argument("--day", "-d", type=int)
    parser.add_argument("--year", "-y", type=int)
    parser.add_argument("--reload", "-r", action='store_true')
    parser.add_argument("--continue", "-c", action='store_true', dest="continue_on_error")
    parser.add_argument("--extra", "-e", action='append')
    parser.add_argument("--skip1", action='store_true')
    parser.add_argument("--skip2", action='store_true')
    parser.add_argument("input_file", nargs='?')
    args = parser.parse_args()

    # Determine the input to use
    if args.line is not None:
        print("Using string '%s' as puzzle input" % args.line)
        puzzle_lines = [ args.line ]
    else:
        # Using input stored in file
        if args.input_file is None:
            # Determine target year and day
            if args.year is None or args.day is None:
                if sys.argv[0][0] == "/":
                    m = re.search(r'^.*\/(\d{4})\/(\d{2})', os.path.normpath(sys.argv[0]))
                else:
                    m = re.search(r'^.*\/(\d{4})\/(\d{2})', os.path.normpath(os.getcwd()+"/"+sys.argv[0]))
                year = datetime.datetime.now().year if m is None else int(m.group(1))
                day = datetime.datetime.now().day if m is None else int(m.group(2))

            # Determine base path of all input files for target day
            args.input_file = os.path.normpath("%s/inputs/%02d" % (os.path.dirname(sys.argv[0]), day))

            if args.sample:
                # Use a sample file (must exist)
                args.input_file += "."+args.sample
            else:
                # Use normal input (will collect it if needed)
                fetch_puzzle_input(year, day, args.input_file, reload=args.reload)

                # First check provided sample solutions if any
                if samples is not None:
                    check_samples(solve_puzzle, samples, args)

        # Finally read input file
        print("Reading puzzle input from %s" % args.input_file)
        with open(args.input_file) as f:
            puzzle_lines = f.read().splitlines()

    # Determine extra arguments
    extra_args = initialize_extra_args(args)

    # Run puzzle with input
    start_ts = int(round(time.time() * 1000))
    answers = solve_puzzle(puzzle_lines, **extra_args)

    answer1 = next(answers)
    answer1_ts = int(round(time.time() * 1000))

    answer2 = next(answers)
    answer2_ts = int(round(time.time() * 1000))

    print("answer1 = %s (%d ms)" % (answer1, answer1_ts-start_ts))
    print("answer2 = %s (%d ms)" % (answer2, answer2_ts-answer1_ts))
