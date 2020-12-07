#!/usr/bin/python3

import aoc

from datetime import datetime
from pytz import timezone
import sys

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
    def __init__(self, lb_id):
        json_lb = aoc.load_leaderboard(lb_id)
        self._id = lb_id
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

    def dump(self):
        for m in self._members:
            print(m)
        print(self._events)

#lb = LeaderBoard(978694)
lb = LeaderBoard(563747)
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
