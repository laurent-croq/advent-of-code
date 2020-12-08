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
            self._stars[d] = {}
            for s in member['completion_day_level'][d]:
                self._stars[d][s] = int(member['completion_day_level'][d][s]['get_star_ts'])
    
    def __repr__(self):
        desc = self._name if self._name is not None else "User #%d" % self._id
        return(desc)
    
    def stars(self):
        _stars = []
        for ts, day, star in [ [ self._stars[d][s], int(d), int(s) ] for d in self._stars for s in self._stars[d] ]:
            _stars.append({ "ts": ts, "day": day, "star": star })
        return(_stars)

class LeaderBoard:
    def __init__(self, lb_id, year=datetime.now().year, cache_dir="leaderboards"):
        self._id = lb_id
        self._year = year
        self._cache_filename = "%s/%s.json" % (cache_dir, str(lb_id))
        json_lb = self._load()
        self._members = [ Member(json_lb['members'][id]) for id in json_lb['members'] ]
        self._events = {}

        for m, stars in [ [ m, m.stars() ] for m in self._members ]:
            m._progress_score = 0
            for s in stars:
                this_event = { "member": m, "day": s['day'], "star": s['star'] }
                if s['ts'] in self._events:
                    self._events[s['ts']].append(this_event)
                else:
                    self._events[s['ts']] = [ this_event ]
        
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

        for ts in sorted(self._events):
            for e in self._events[ts]:
                e['points'] = star_rewards[e['day']][e['star']]['points']
                e['rank'] = star_rewards[e['day']][e['star']]['rank']

                e['member']._progress_score += e['points']
                e['score'] = e['member']._progress_score
                e['global_rank'] = 1+len([ m for m in self._members if m._progress_score > e['member']._progress_score ])

                star_rewards[e['day']][e['star']]['points'] = max(star_rewards[e['day']][e['star']]['points']-1, 0)
                star_rewards[e['day']][e['star']]['rank'] += 1

    def _load(self):
        cache_file = pathlib.Path(self._cache_filename)
        if cache_file.exists():
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

    def dump(self, day):
        board = []
        for ts in sorted(self._events):
            for e in [ e for e in lb._events[ts] if lb._events[e]['day'] == day ][-1]:
                board.append([ e['member'], e['star'], e['global_rank'], e['score'] ])

        for l in sorted(board, key=lambda l: l['score']):
            print("%02d %-30s %d stars / %3 pts" % (l['global_rank'], l['member'], l['star'], l['score']))

#lb = LeaderBoard(978694)
lb = LeaderBoard(563747)
lb.dump(8)
exit(0)
for m in lb._members:
    print(m)

for ts in sorted(lb._events):
    for e in lb._events[ts]:
        print("%-14s %-30s #%2d %4d pts | Day %2d, star %d (#%2d: +%2d pts) " % (
            datetime.fromtimestamp(ts, tz=timezone('EST')).strftime("%d %H:%M:%S"),
            e['member'],
            e['global_rank'],
            e['score'],
            e['day'],
            e['star'],
            e['rank'],
            e['points']
            )
        )

for m in [ m for m in lb._members if m._score != m._progress_score ]:
    print("Score mismatch for %s: ends with %d instead of %d" % (m, m._progress_score, m._score))
