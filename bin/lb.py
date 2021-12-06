#!/usr/bin/env python3.8

from datetime import datetime
from pytz import timezone
from time import time

import pathlib, sys, re, requests, os, json, argparse

class Member:
    def __init__(self, member):
        self._id = int(member['id'])
        self._name = member['name']
        self._score = member['local_score']
        self._stars = {}
        self._progress_score = 0
        for d in member['completion_day_level']:
            self._stars[int(d)] = {}
            for s in member['completion_day_level'][d]:
                self._stars[int(d)][int(s)] = { "ts": int(member['completion_day_level'][d][s]['get_star_ts']) }
    
    def __str__(self):
        return(self._name if self._name is not None else "User #%d" % self._id)
    
    def __repr__(self):
        return(self._id)
    
    def stars(self):
        _stars = []
        for day, star in [ [ int(d), int(s) ] for d in self._stars for s in self._stars[d] ]:
            _stars.append({ "ts": self._stars[day][star]['ts'], "day": day, "star": star })
        return(_stars)

class LeaderBoard:
    def __init__(self, lb_id, session_id, year=datetime.now().year, cache_dir=".leaderboards", reload=False):
        if lb_id is None:
            print("Missing leaderboard ID (use -b option or AOC_LEADERBOARD_ID environment variable")
            sys.exit(1)

        self._id = int(lb_id)
        self._session_id = session_id
        self._year = int(year)
        self._cache_filename = "%s/%d-%d.json" % (cache_dir, self._id, self._year)

        json_lb = self._load(reload=reload)
        self._members = [ Member(json_lb['members'][id]) for id in json_lb['members'] ]
        self._events = []

        # Initialize events (1 event per collected star by each member) and sort them by timestamp
        for m, s in [ [ m, s ] for m in self._members for s in m.stars() ]:
            self._events.append({ "ts": s['ts'], "member": m, "day": s['day'], "star": s['star'] })

        self._events = sorted(self._events, key=lambda e: e['ts'])

        # Initialize star rewards per day
        star_rewards = {}
        for day in range(1, 26):
            star_rewards[day]= {
                1: { "points": len(self._members), "rank": 1 },
                2: { "points": len(self._members), "rank": 1 }
            }

        # Complete each event
        for e in self._events:
            e['points'] = star_rewards[e['day']][e['star']]['points']
            e['rank'] = star_rewards[e['day']][e['star']]['rank']

            e['member']._progress_score += e['points']
            e['score'] = e['member']._progress_score
            e['global_rank'] = 1+len([ m for m in self._members if m._progress_score > e['member']._progress_score ])

            e['member']._stars[e['day']][e['star']]['points'] = e['points']
            e['member']._stars[e['day']][e['star']]['rank'] = e['rank']
            e['member']._stars[e['day']][e['star']]['global_rank'] = e['global_rank']

            # Update next star rewards for this day
            star_rewards[e['day']][e['star']]['points'] = max(star_rewards[e['day']][e['star']]['points']-1, 0)
            star_rewards[e['day']][e['star']]['rank'] += 1

    def _load(self, reload=False):
        cache_file = pathlib.Path(self._cache_filename)
        if cache_file.exists() and not reload and (time() - cache_file.stat().st_mtime) <= 60*15:
            print("Using leaderboard cache %s" % self._cache_filename)
            with open(self._cache_filename) as f:
                return(json.loads(f.read()))

        lb_url = "https://adventofcode.com/%d/leaderboard/private/view/%d.json" % (self._year, self._id)
        if self._session_id is None:
            print("Missing session ID (use -s option or AOC_SESSION_ID environment variable")
            sys.exit(1)

        print("Fetching leaderboard #%d from %s" % (self._id, lb_url))
        with requests.get(lb_url, cookies={"session": self._session_id}) as r:
            if r.status_code == 302:
                print("Got 302 : bad session_id ?")
                sys.exit(1)
            elif r.status_code == 404:
                print("Got 404 : leaderboard not found")
                sys.exit(1)
            r.raise_for_status()
            try:
                with open(self._cache_filename, 'w') as f:
                    f.write(r.text)
            except:
                print("Failed to create %s" % self._cache_filename)
            return(json.loads(r.text))

    def dump_ranking(self, day=None):
        if day is None:
            first_day = 1
            last_day = 25
        else:
            m = re.search(r'^(\d+)[:-](\d+)$', day)
            if m is not None:
                first_day = int(m.group(1))
                last_day = int(m.group(2))
            else:
                first_day = 1
                last_day = int(day)

        ranking = {}
        for e in [ e for e in self._events if e['day'] in range(first_day, last_day+1) ]:
            if e['member'] in ranking:
                ranking[e['member']]['points'] += e['points']
                ranking[e['member']]['rank'] = e['rank']
                ranking[e['member']]['stars'] += 1
            else:
                ranking[e['member']] = { 'points': e['points'], 'rank': e['rank'], 'stars': 1 }

        rank = 1
        prev_points = None
        for m in sorted(ranking, key=lambda m: ranking[m]['points'], reverse=True):
            rank += (prev_points is not None and ranking[m]['points'] != prev_points)
            print("%2s %-30s %4d points, %2d stars : %s" % (
                rank if ranking[m]['points'] != prev_points else "|",
                m,
                ranking[m]['points'],
                ranking[m]['stars'],
                "*" * ranking[m]['stars']
                )
            )
            prev_points = ranking[m]['points']

        print("%s players" % (len(self._members)))

    def dump_events(self, user=None, localtime=False, all=False):
        last_ts = None
        last_day = None
        tz = timezone('CET' if localtime else 'EST')
        today = datetime.now(timezone('EST')).strftime("%d")
        for e in self._events :
            if user is not None and str(e['member']).lower().find(user) < 0:
                continue

            this_day = datetime.fromtimestamp(e['ts'], timezone('EST')).strftime("%d")
            if not all and this_day != today:
                continue

            if last_day is not None and this_day != last_day:
                print("_" * 100)
            last_day = this_day
            this_ts = datetime.fromtimestamp(e['ts'], tz).strftime("%Y/%m/%d %H:%M:%S")
            if last_ts is not None and this_ts == last_ts:
                this_ts = ""
            else:
                last_ts = this_ts

            print("%-19s %-30s #%2d on star %2d#%d = +%2d pts | General #%2d with %4d pts" % (
                this_ts,
                e['member'],
                e['rank'],
                e['day'],
                e['star'],
                e['points'],
                e['global_rank'],
                e['score']
                )
            )
        
        today_events = [ e for e in self._events if e['day'] == int(today) ]
        print("%s players, next stars: 1=%d pts, 2=%d pts" % (
            len(self._members), 
            max(0, len(self._members)-len([ e['points'] for e in today_events if e['star'] == 1 and e['points']>0 ])),
            max(0, len(self._members)-len([ e['points'] for e in today_events if e['star'] == 2 and e['points']>0 ]))
            )
        )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session_id", "-s", default=os.environ.get('AOC_SESSION_ID', None))
    parser.add_argument("--leaderboard_id", "-l", type=int, default=os.environ.get('AOC_LEADERBOARD_ID', None))
    parser.add_argument("--year", "-y")
    parser.add_argument("--day", "-d")
    parser.add_argument("--user", "-u")
    parser.add_argument("--events", "-e", action='store_true')
    parser.add_argument("--est", "-z", dest="localtime", action='store_false')
    parser.add_argument("--all", "-a", action='store_true')
    parser.add_argument("--reload", "-r", action='store_true')

    args = parser.parse_args()

    if args.year is None:
        m = re.search(r'^.*\/(\d{4})\/', os.path.normpath(os.getcwd()+"/"+sys.argv[0]))
        args.year = int(m.group(1)) if m is not None else datetime.now().year

    lb = LeaderBoard(args.leaderboard_id, args.session_id, year=args.year, reload=args.reload, cache_dir=os.path.normpath(sys.argv[0]+"/../../.leaderboards"))

    if args.events:
        lb.dump_events(user=args.user, localtime=args.localtime, all=args.all)
    else:
        lb.dump_ranking(args.day)

if __name__ == "__main__":
    main()

