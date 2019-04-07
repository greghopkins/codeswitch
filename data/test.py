import json
from client import Session, Locator

s = Session()
l = Locator()

# get mom and home
results = s.query(moms=[{"name": "Margaret Herrera"}])
mom = results['moms'][0]
location = l.to_geojson(l.locate(mom['home']))

# get services
by_services= s.query(providers=[{
    "services.type": "Child care",
}])
# print("Child care results:\n{}".format(json.dumps(by_services, indent=4)))
print("{} child care results".format(len(by_services['providers'])))

# get nearby
nearby = s.query(providers=[{
    "location": {"geojson": location, "radius": 3}
}])
# print("Nearby child care results:\n{}".format(json.dumps(nearby, indent=4)))
print("{} nearby results".format(len(nearby['providers'])))

# get nearby services
nearby_services = s.query(providers=[{
    "services.type": "Child care",
    "location": {"geojson": location, "radius": 3}
}])

# print("Nearby child care results:\n{}".format(json.dumps(nearby_services, indent=4)))
print("{} nearby child care results".format(len(nearby_services['providers'])))

# get nearby services
my_results = s.query(providers=[{
    "services.type": "Child care",
    "values": mom['values'],
    "location": {"geojson": location, "radius": 3}
}])

print("{} nearby child care results that match some of my values:\n{}".format(
    len(my_results['providers']),
    json.dumps(my_results['providers'], indent=4)
))
