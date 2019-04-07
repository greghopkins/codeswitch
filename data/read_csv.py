#!/usr/bin/env python3

import csv
import json
from random import choice

from client import Session, Locator

locator = Locator()
session = Session()

with open('data.tsv', 'r') as f:
    data_reader = csv.reader(f, delimiter='\t')
    entries = []
    for row in data_reader:
        # parse services
        services = session.query(services=[{"type": row[2]}])
        service_entries = []
        if services['services']:
            service_subtypes = [st.strip() for st in row[3].split(',')]
            service_types = [s for s in services['services'] if len(set(s['subtypes']).intersection(service_subtypes)) != 0]
            for s in service_types:
                for st in set(s['subtypes']).intersection(service_subtypes):
                    service_entries.append({"type": s["type"], "subtype": st})

        # parse location
        address = row[4].split(',')
        location = {
            'zip': address.pop(-1).strip(),
            'state': address.pop(-1).strip(),
            'city': address.pop(-1).strip()
        }
        for i, street in enumerate(address):
            location['street{}'.format(i+1)] = street.strip()
        geolocation = locator.locate(location)

        # parse hours
        availability={}
        if row[9].strip():
            time_groups = [[t.strip() for t in s.split(",")] for s in row[9].split(";")]
            availability = [
                {"from": t[0], "to": t[1], "dow": t[2]} for t in time_groups
            ]

        # simulate value tags
        value_tags = []
        values = session.sample("values")
        for v in values['values']:
            if 'subtypes' not in v and v['type'] not in [vt['type'] for vt in value_tags]:
                value_tags.append({'type': v['type']})
            else:
                for _ in range(0, session.count()):
                    subtype = choice(v['subtypes'])
                    if (v['type'], subtype) not in [(vt['type'], vt.get('subtype')) for vt in value_tags]:
                        value_tags.append({
                            'type': v['type'],
                            'subtype': subtype,
                        })

        entries.append({
            "name": row[0],
            "organization": row[1],
            "phone": row[5],
            "website": row[8],
            "description": row[10],
            "emergency": False,
            "services": service_entries,
            "address": address,
            "location": locator.to_geojson(geolocation),
            "availability": availability,
            "value_tags": value_tags
        })

    session.insert(providers=entries)
