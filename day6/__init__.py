

class Day06(object):
    def __init__(self, read_file_fn):
        self.data = read_file_fn('day6').split('\n')[:-1]
        # self.data = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']

    def run_solution1(self):
        """
        :return:
        """
        universal_orbit_map = UniversalOrbitMap(self.data)
        return universal_orbit_map.run_program()

    def run_solution2(self):
        """
        :return:
        """
        universal_orbit_map = UniversalOrbitMap(self.data)
        universal_orbit_map.run_program()
        return universal_orbit_map.shortest_path('YOU', 'SAN')


class UniversalOrbitMap(object):
    def __init__(self, data):
        self.orbit_map = self.generate_orbit_map(data)
        self.orbit_paths = {}

    @staticmethod
    def generate_orbit_map(raw):
        orbit_map = {}
        for item in raw:
            map_split = item.split(')')
            if orbit_map.get(map_split[0], False):
                orbit_map[map_split[0]].append(map_split[1])
            else:
                orbit_map[map_split[0]] = [map_split[1]]
            if orbit_map.get(map_split[1], False):
                pass
            else:
                orbit_map[map_split[1]] = []
        return orbit_map

    def run_program(self):
        orbit_count = self.calculate_orbit_count()
        return orbit_count

    def calculate_orbit_count(self):
        orbits_object = {}
        orbit_values = list(self.orbit_map.values())
        orbit_keys = list(self.orbit_map.keys())
        total_counter = 0
        for key in orbit_keys:
            pointer = key
            orbit_list = []
            while pointer != 'COM':
                for i, item in enumerate(orbit_values):
                    if pointer in item:
                        pointer = orbit_keys[i]
                        orbit_list.append(pointer)
            orbits_object[key] = {'orbit_count': len(orbit_list), 'orbit_list': orbit_list.copy()}
            total_counter += len(orbit_list)
            # print(f'{key} direct orbits: {orbits_object[key]}')
        self.orbit_paths = orbits_object
        return total_counter

    def shortest_path(self, origin, destination):
        print(f'origin: {origin}\n{self.orbit_paths[origin]}')
        print(f'origin: {destination}\n{self.orbit_paths[destination]}')
        print(f'Finding shortest path!')
        shortest_path = []
        found_intersection = False
        intersection_planet = ''
        for planet_object in self.orbit_paths[origin]['orbit_list']:
            shortest_path.append(planet_object)
            for planet_object2 in self.orbit_paths[destination]['orbit_list']:
                if planet_object == planet_object2:
                    print(f'Found intersection at planet {planet_object}')
                    intersection_planet = planet_object
                    found_intersection = True
                    break
            if found_intersection:
                break
        destination_intersection_index = self.orbit_paths[destination]['orbit_list'].index(intersection_planet)
        destination_orbit_list_from_intersection = self.orbit_paths[destination]['orbit_list'][0: destination_intersection_index][::-1]
        shortest_path.extend(destination_orbit_list_from_intersection)
        print(shortest_path)
        number_of_transfers = len(shortest_path) - 1
        return number_of_transfers
