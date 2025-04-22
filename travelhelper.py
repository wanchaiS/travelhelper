import os
import sys

# https://stackoverflow.com/a/35904211
this = sys.modules[__name__]
this.routes = []

def main():
    """
     Main function where the magic happen!
    """

    validate_args()

    option = sys.argv[1]

    file = get_file(option)

    read_file(file)

    match option:
        case '-a':
            run_mode_a()
        case '-o':
            run_mode_o()
        case '-d':
            run_mode_d()
        case '-v':
            run_mode_v()
        case _:
            print(f"Unsupported option! '{option}'")
            exit(1)
    return

def validate_args():
    # less than 2 argument provided  index 0 = python file
    if len(sys.argv) < 3:
        print("A script must be executed with arguments travelhelper.py [-a | -o | -d | -v] argument_file.")
        exit(1)
    
    # argument requirement basd on option
    option = sys.argv[1]
    match option:
        case "-v" | "-a":
            # no need further validation the extra argument can be ignored
            return
        case "-d" | "-o":
            if len(sys.argv) < 4:
                print("Option '-o' | '-d' must follow by a city or distance")
                exit(1)
            return
        case _:
            print(f"Option '{option}' is not supported!")
    

def get_file(option):
    if option in ['-a','-v']:
        file = sys.argv[2]
        # validate file
        validate_file(file)
        return file
    
    if option in ['-o','-d']:
        file = sys.argv[3]
        # validate file
        validate_file(file)
        return file

    print(f"Unsupported option! '{option}'")
    exit(1)

def validate_file(file):
    if not file:
        print("Missing an argument for a file!")
        exit(1)
    if not os.path.exists(file):
        print(f"File '{file}' does not exist!") 
        exit(1)
    if not os.path.isfile(file):
        print(f"File '{file}' is not a file!")
        exit(1)
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

def run_mode_o():

    # safe to assume position because option and file has been validated
    origin_input = sys.argv[2]

    filteredRoutes = [r for r in this.routes if r["origin"] == origin_input]
    if len(filteredRoutes) == 0:
        print(f"No known destinations from {origin_input}")
        return
    
    print(f"Destinations from {origin_input}:")
    for route in filteredRoutes:
        print(f"City: {route['destination']}")
        print(f"Distance: {route['distance']}")


def run_mode_d():
    distance_input = sys.argv[2]

    try:
        distance = int(distance_input)
        if not isinstance(distance, int):
            print(f"Distance {distance} is not integer")
            exit(1)
        if distance < 0:
            print("Distance cannot be negative!")
            exit(1)
    except Exception as e:
        print(f"Unable to parse distance {distance_input} into int, Error message: {e}")
        exit(1)

    filteredRoutes = [r for r in this.routes if int(r["distance"]) <= distance]
    if len(filteredRoutes) == 0:
        print(f"No cities within {distance} Km")
        return
    
    print(f"Cities within {distance} Km distance:")
    for route in filteredRoutes:
        print(f"{route['origin']}-{route['destination']}")
        print(f"Distance: {route['distance']}")



def read_file(file):
    try:
        with open(file, 'r') as f:
            for line in f:
                # Remove leading/trailing whitespace
                processed_line = line.strip() 
                # construct an object of route
                parts = processed_line.split(",")
                route = {"origin":parts[0] , "destination":parts[1], "distance":parts[2]}
                this.routes.append(route)
                # Your line processing logic here
    except Exception as e:
        print(f"An error occurred while reading the file '{file}': {e}")

if __name__ == "__main__":
    main()
