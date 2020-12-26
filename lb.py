#!/usr/bin/python3

from datetime import datetime
from pytz import timezone
from time import time

import pathlib, sys, re, requests, os, json

class Member:
    def __init__(self, member):
        self._id = int(member['id'])
        self._name = member['name']
        self._score = member['local_score']
        self._stars = {}
        for d in member['completion_day_level']:
            self._stars[int(d)] = {}
            for s in member['completion_day_level'][d]:
                self._stars[int(d)][int(s)] = { "ts": int(member['completion_day_level'][d][s]['get_star_ts']) }
    
    def __str__(self):
        desc = self._name if self._name is not None else "User #%d" % self._id
        return(desc)
    
    def __repr__(self):
        return(self._id)
    
    def stars(self):
        _stars = []
        for day, star in [ [ int(d), int(s) ] for d in self._stars for s in self._stars[d] ]:
            _stars.append({ "ts": self._stars[day][star]['ts'], "day": day, "star": star })
        return(_stars)

class LeaderBoard:
    def __init__(self, lb_id, year=datetime.now().year, cache_dir="leaderboards", reload=False):
        self._id = lb_id
        self._year = year
        self._cache_filename = "%s/%s.json" % (cache_dir, str(lb_id))
        json_lb = self._load(reload=reload)
        self._members = [ Member(json_lb['members'][id]) for id in json_lb['members'] ]
        self._events = []

        for m in self._members:
            m._progress_score = 0
            for s in m.stars():
                self._events.append({ "ts": s['ts'], "member": m, "day": s['day'], "star": s['star'] })

        self._events = sorted(self._events, key=lambda e: e['ts'])

        # Initialize star rewards per day (day #1 is an exception: no reward)
        star_rewards = { 1: {
            1: { "points": 0, "rank": 1 },
            2: { "points": 0, "rank": 1 }
        }}

        for day in range(2, 26):
            star_rewards[day]= {
                1: { "points": len(self._members), "rank": 1 },
                2: { "points": len(self._members), "rank": 1 }
            }

        for e in self._events:
            e['points'] = star_rewards[e['day']][e['star']]['points']
            e['rank'] = star_rewards[e['day']][e['star']]['rank']

            e['member']._progress_score += e['points']
            e['score'] = e['member']._progress_score
            e['global_rank'] = 1+len([ m for m in self._members if m._progress_score > e['member']._progress_score ])

            e['member']._stars[e['day']][e['star']]['points'] = e['points']
            e['member']._stars[e['day']][e['star']]['rank'] = e['rank']
            e['member']._stars[e['day']][e['star']]['global_rank'] = e['global_rank']

            star_rewards[e['day']][e['star']]['points'] = max(star_rewards[e['day']][e['star']]['points']-1, 0)
            star_rewards[e['day']][e['star']]['rank'] += 1

    def _load(self, reload=False):
        cache_file = pathlib.Path(self._cache_filename)
        if cache_file.exists() and not reload:
            if time() - cache_file.stat().st_mtime <= 60*15:
                print("Using leaderboard cache %s" % self._cache_filename)
                with open(self._cache_filename) as f:
                    return(json.loads(f.read()))

        lb_url = "https://adventofcode.com/%d/leaderboard/private/view/%d.json" % (int(self._year), int(self._id))
        try:
            session_id = os.environ['AOC_SESSION_ID']
        except KeyError:
            print("AOC_SESSION_ID environment variable is not defined")
            sys.exit(1)

        print("Fetching leaderboard #%d from %s" % (self._id, lb_url))
        with requests.get(lb_url, cookies={"session": session_id}) as r:
            if r.status_code == 302:
                print("Got a 302 : leaderboard not found or bad session_id ?")
                sys.exit(1)
            r.raise_for_status()
            try:
                with open(self._cache_filename, 'w') as f:
                    f.write(r.text)
            except:
                print("Failed to create %s" % self._cache_filename)
            return(json.loads(r.text))

    def dump_ranking(self, day=None):
        first_day = 1
        last_day = 25
        if day is not None:
            m = re.search(r'^(\d+)[:-](\d+)$', day)
            if m is not None:
                first_day = int(m.group(1))
                last_day = int(m.group(2))
            else:
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
            if prev_points is not None and ranking[m]['points'] != prev_points:
                rank += 1
            print("%2s %-30s %4d points, %2d stars : %s" % (rank if ranking[m]['points'] != prev_points else "|", m, ranking[m]['points'], ranking[m]['stars'], "*" * ranking[m]['stars']))
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
            this_ts = datetime.fromtimestamp(e['ts'], tz).strftime("%d %H:%M:%S")
            if last_ts is not None and this_ts == last_ts:
                this_ts = ""
            else:
                last_ts = this_ts

            print("%-12s %-30s #%2d on star %2d/%d = +%2d pts | General #%2d with %4d pts" % (
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
        next_points_1 = max(0, len(self._members)-len([ e['points'] for e in today_events if e['star'] == 1 and e['points']>0 ]))
        next_points_2 = max(0, len(self._members)-len([ e['points'] for e in today_events if e['star'] == 2 and e['points']>0 ]))
        print("%s players, next stars: 1=%d pts, 2=%d pts" % (len(self._members), next_points_1, next_points_2))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--id", type=int, default=563747)
parser.add_argument("--day", "-d")
parser.add_argument("--events", "-e", action='store_true')
parser.add_argument("--localtime", "-l", action='store_true')
parser.add_argument("--all", "-a", action='store_true')
parser.add_argument("--reload", "-r", action='store_true')
parser.add_argument("--year", "-y")
parser.add_argument("--user", "-u")

args = parser.parse_args()

#lb = LeaderBoard(978694)
if args.year is None:
    m = re.search(r'^.*\/(\d{4})\/', os.path.normpath(os.getcwd()+"/"+sys.argv[0]))
    args.year = int(m.group(1)) if m is not None else datetime.now().year

lb = LeaderBoard(args.id, year=args.year, reload=args.reload)

if args.events:
    lb.dump_events(user=args.user, localtime=args.localtime, all=args.all)
else:
    lb.dump_ranking(args.day)

