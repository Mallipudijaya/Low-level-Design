from collections import deque

class Person:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def getAllConnections(self):
        # Returns the list of direct connections (friends) for this person
        return self.connections

def shortestPath(personA, personB):
    if personA == personB:
        return [personA.name]

    # BFS queue to store (current person, path to that person)
    queue = deque([(personA, [personA.name])])
    
    # Set to track visited people
    visited = set([personA])
    
    while queue:
        currentPerson, path = queue.popleft()
        
        # Check all direct connections (friends) of the current person
        for neighbor in currentPerson.getAllConnections():
            if neighbor == personB:
                return path + [neighbor.name]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor.name]))
    
    # If no path is found, return an empty list
    return []

# Example usage:
if __name__ == "__main__":
    # Create people
    personA = Person("A")
    personB = Person("B")
    personC = Person("C")
    personD = Person("D")
    personE = Person("E")
    personG = Person("G")

    # Create connections
    personA.connections = [personB, personD, personE]
    personB.connections = [personE, personG]
    personD.connections = [personC]
    personE.connections = [personG]

    # Find the shortest path between personA and personG
    path = shortestPath(personA, personG)
    print("Shortest path:", path)  # Output: ['A', 'B', 'G']
