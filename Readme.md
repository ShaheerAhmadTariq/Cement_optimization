

# Concrete Mix Optimization using Genetic Algorithm

## Description

This project utilizes Genetic Algorithms (GAs) to optimize concrete mixtures based on desired properties such as CO2 emissions, cost, and strength. It incorporates predictive models for CO2 emissions, cost, and strength to guide the optimization process.

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/ShaheerAhmadTariq/Cement_optimization.git
   cd Cement_optimization
   ```

2. Install the required Python libraries:

   ```shell
   pip install pygad numpy joblib pandas
   ```

## Usage

1. Load the trained predictive models for CO2 emissions, cost, and strength using joblib:

   ```python
   import joblib

   rf_model_cost = joblib.load('rf_model_cost.pkl')
   rf_model_strength = joblib.load('rf_model_strength.pkl')
   rf_model_co2 = joblib.load('rf_model_co2.pkl')
   ```

2. Define the desired property values for CO2 emissions, cost, and strength:

   ```python
   desired_co2 = 88.34
   desired_cost = 41.5
   desired_strength = 90
   ```

3. Specify the fitness weights for each property to guide the optimization:

   ```python
   weights = [0.5, 0.1, 0.4]
   ```

4. Define gene ranges for the concrete mixture components:

   ```python
   gene_ranges = [(102.0, 540.0),  # Cement
                 (0.0, 359.4),   # Blast Furnace Slag
                 (0.0, 200.1),   # Fly Ash
                 (121.8, 247.0), # Water
                 (0.0, 32.2),    # Superplasticizer
                 (801.0, 1145.0),# Coarse Aggregate
                 (594.0, 992.6), # Fine Aggregate
                 (1.0, 365.0)]   # Age
   ```

5. Run the Genetic Algorithm with the specified configuration:

   ```python
   # Create and run the GA instance
   ga_instance = pygad.GA(**ga_config)
   ga_instance.run()
   ```

6. Retrieve the details of the best solution:

   ```python
   solution, solution_fitness, solution_idx = ga_instance.best_solution()
   print("Parameters of the best solution : {solution}".format(solution=solution))
   print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
   print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
   ```

7. Predict property values based on the best solution:

   ```python
   c02_prediction = rf_model_co2.predict(pd.DataFrame([solution], columns=['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water', 'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate', 'Age']))[0]
   strength_prediction = rf_model_strength.predict(pd.DataFrame([solution], columns=['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water', 'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate', 'Age']))[0]
   cost_prediction = rf_model_cost.predict(pd.DataFrame([solution], columns=['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water', 'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate', 'Age']))[0]
   print("Predicted output based on the best solution \nco2:  {prediction} \n cost: {cost_prediction} \n strength: {strength_prediction}".format(prediction=c02_prediction, cost_prediction=cost_prediction, strength_prediction=strength_prediction))
   ```

8. Customize other parameters and configurations as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, issues, or contributions, please contact:

- [Shaheer Ahmad Tariq](mailto:shaheerahmadtariq@gmail.com)

---
