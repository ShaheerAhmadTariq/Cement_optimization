import json
import numpy
with open('fitness_history.json', 'r') as json_file:
    fitness_history = json.load(json_file)
    print(fitness_history["844"])

# weights = [1.0, -1.0, -1.0]
# weighted_fitness = numpy.dot(weights, [0.0425176047029764, 0.26923437765450337, 11.928187619456512])   

# print(weighted_fitness)