import sys
import argparse
import pathlib

# https://stackoverflow.com/a/35904211
this = sys.modules[__name__]
this.routes = []

def main():
    """
     Main function where the magic happen!
    """
    payload = parse_args()

    validate_file(payload["file"])
    
    read_file(payload["file"])

    if payload["mode"] == "a":
        run_mode_a()

    elif payload["mode"] == "v":
        run_mode_v()

    elif payload["mode"] == "o":
        run_mode_o(payload["value"])

    elif payload["mode"] == "d":
        run_mode_d(payload["value"])
    
    return

def run_mode_a():
    if len(this.routes) == 0:
        print("No distance information in this file")
        return

    print("Origin-destination cities:")
    for route in this.routes:
        print(f'{route["origin"]}-{route["destination"]}')

def run_mode_v():
    print("Name: Wanchai")
    print("SurName: Sangkusolwong")
    print("StudentId: 25654120")
    print("Date of completion: xxx")

def run_mode_o(origin_input):
    filteredRoutes = [r for r in this.routes if r["origin"] == origin_input]
    if len(filteredRoutes) == 0:
        print(f"No known destinations from {origin_input}")
        return
    
    print(f"Destinations from {origin_input}:")
    for route in filteredRoutes:
        print(f"City: {route['destination']}")
        print(f"Distance: {route['distance']}")

def run_mode_d(distance_input):
    filteredRoutes = [r for r in this.routes if int(r["distance"]) <= distance_input]
    if len(filteredRoutes) == 0:
        print(f"No cities within {distance_input} Km")
        return
    
    print(f"Cities within {distance_input} Km distance:")
    for route in filteredRoutes:
        print(f"{route['origin']}-{route['destination']}")
        print(f"Distance: {route['distance']}")

def parse_args():
    """
    Define arguments and parse
    source: https://stackoverflow.com/a/30493366 , https://docs.python.org/3/library/argparse.html#type
    """

    # define helpful description of the script
    parser = argparse.ArgumentParser(
    description="A travel helper that helps inquiry about distance of cities.")

    # Required positional argument
    parser.add_argument('argument_file',type=pathlib.Path, help='a file that contains cities and distances data (required)')
    # group options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a',action="store_true", help='list all origin-destination cities')
    group.add_argument('-o', metavar="city", nargs=1,help='list all the routes that has this given city as an origin')
    group.add_argument('-d',metavar="distance", nargs=1,type=int,help='list all the routes that its distance is in between given distance')
    group.add_argument('-v',action="store_true", help='display student information')

    args = parser.parse_args()

    mode=None
    value=None
    if args.a:
        mode = "a"
    elif args.v:
        mode = "v"
    elif args.o:
        mode = "o"
        value = args.o[0]
    elif args.d:
        mode = "d"
        value = args.d[0]

    return {"mode": mode,"value": value,"file": args.argument_file}


def validate_file(_file):
    if not _file.exists():
        print(f"'{_file}' does not exist.")
        exit(1)
    if not _file.is_file():
        print(f"'{_file}' is not a file.")
        exit(1)

def read_file(_file):
    try:
        with open(_file, 'r') as f:
            for line in f:
                # Remove leading/trailing whitespace
                processed_line = line.strip() 
                # construct an object of route
                parts = processed_line.split(",")
                route = {"origin":parts[0] , "destination":parts[1], "distance":parts[2]}
                this.routes.append(route)
                # Your line processing logic here
    except Exception as e:
        print(f"An error occurred while reading the file '{_file}': {e}")
    

if __name__ == "__main__":
    main()
