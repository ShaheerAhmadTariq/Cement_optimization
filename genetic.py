import pygad
import numpy 
import json


# Coefficients for the formulas
co2_coefficients = [7.66660000e-01, 2.65000000e-02, 1.96000000e-02, -1.70000000e-04, 7.82400000e-01, 2.90000000e-03, 3.70000000e-03, 1.97758476e-16]
cost_coefficients = [8.11400000e-02, 1.05838800e+01, 1.41120000e-01, -6.40000000e-04, 4.93910000e-01, 1.41100000e-02, 1.05800000e-02, 3.10862447e-15]
strength_coefficients = [0.11753383, 0.1055869, 0.08173688, -0.14507647, 0.30658023, 0.01683671, 0.02012234, 0.11563608]

desired_co2 = 88.34
desired_cost = 41.5
desired_strength = 90
weights = [0.9, -0.05, -0.05]
# weights = [1,1,1]

fitness_history = {}
S_Intercept = -22.243374861043932
COST_Intercept = 2.9558577807620168e-12
co2_Intercept = 4.831690603168681e-13



gene_range = [(102.0, 540.0), # Cement
              (0.0, 359.4), # Blast Furnace Slag
              (0.0, 200.1), # Fly Ash
              (121.8, 247.0), # Water (Assuming these limits, you can adjust as per your data)
              (0.0, 32.2), # Superplasticizer
              (801.0, 1145.0), # Coarse Aggregate
              (594.0, 992.6), # Fine Aggregate
              (1.0, 365.0)] # Age (Assuming a max age of 1 year)

def repair_solution(solution):
    return numpy.maximum(solution, 0)

def fitness_function(ga_instance, solution, solution_idx):
    # repaired_solution = repair_solution(solution)
    repaired_solution = solution

    co2 = numpy.sum(repaired_solution * co2_coefficients) + co2_Intercept
    cost = numpy.sum(repaired_solution * cost_coefficients) + COST_Intercept
    strength = numpy.sum(repaired_solution * strength_coefficients) + S_Intercept
    fitness_co2 = co2 - desired_co2
    fitness_cost = cost - desired_cost
    fitness_strength = 1.0 / numpy.abs(strength - desired_strength)
    fitness_history[ga_instance.generations_completed] = [fitness_co2, fitness_cost, fitness_strength]
    weighted_fitness = numpy.dot(weights, [fitness_strength, fitness_cost, fitness_co2])    
    return weighted_fitness

fitness_function = fitness_function

num_generations = 500 # Number of generations.
num_parents_mating = 14 # Number of solutions to be selected as parents in the mating pool.

sol_per_pop = 100 # Number of solutions in the population.
num_genes = len(co2_coefficients)

last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    last_fitness = ga_instance.best_solution()[1]


ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       parent_selection_type="rws",
                       mutation_type="adaptive",
                       allow_duplicate_genes=False,
                    #    initial_population=initial_population,
                       mutation_percent_genes = [25, 12],
                       sol_per_pop=sol_per_pop, 
                       crossover_type="uniform",
                       gene_space=gene_range,
                       stop_criteria="saturate_100",
                       num_genes=num_genes,
                       on_generation=callback_generation)

print(ga_instance.initial_population)
ga_instance.run()
# ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

c02_prediction = numpy.sum(numpy.array(co2_coefficients)*solution)
strength_prediction = numpy.sum(numpy.array(strength_coefficients)*solution)
cost_prediction = numpy.sum(numpy.array(cost_coefficients)*solution)
# print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))
print("Predicted output based on the best solution \nco2:  {prediction} \n cost: {cost_prediction} \n strength: {strength_prediction}".format(prediction=c02_prediction, cost_prediction=cost_prediction, strength_prediction=strength_prediction))
# with open('fitness_history.json', 'w') as json_file:
#     json.dump(fitness_history, json_file)
# print("fitness values of the last population: {last_fitness}".format(last_fitness=ga_instance.last_generation_fitness))
if ga_instance.best_solution_generation != -1:
    print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

