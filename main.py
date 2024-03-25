import csv 
import random 

# Reading the CSV file 
def read_csv(file_path): 
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Analyze the Sample Data 
def analyse_data(data): 
    # Analysing the frequencies of the attributes and calculating the probabilities required for generating the synthetic dataset
    frequency_count = {} 
    total_population = len(data)
    for row in data: 
        for key, value in row.items(): 
            if key not in frequency_count:
                frequency_count[key] ={}
            if value not in frequency_count[key]: 
                frequency_count[key][value] = 0
            frequency_count[key][value] += 1
    probabilities = {} 
    for key, value_counts in frequency_count.items(): 
        probabilities[key] = {value: count/total_population for value, count in value_counts.items()}
    return probabilities

# Generating the Synthetic Population 
def generate_population(sample_data, population_size): 
    synthetic_pop = []
    for _ in range(population_size):
        agent = {} 
        for attribute, probabilities in sample_data.items(): 
            agent[attribute] = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]
        synthetic_pop.append(agent)
    return synthetic_pop

# Computing Frequencies 
def compute_frequencies(population): 
    # Calc the frequencies of attributes in the synthetic population 
    frequencies = {}
    for agent in population:
        for attribute, value in agent.items():
            if attribute not in frequencies:
                frequencies[attribute] = {}
            if value not in frequencies[attribute]:
                frequencies[attribute][value] = 0
            frequencies[attribute][value] += 1
    return frequencies

# Writing output to a Text file 
def write_to_output_file(frequencies, output_file): 
    #Write the computed frequencies into a text file in the required format 
    with open(output_file, 'w') as file: 
        # Convert category numbers to actual category names
        sex_mapping = {1: 'Male', 2: 'Female'}
        age_mapping = {1: 'Below 22 years', 2: '22-60 years', 3: 'Above 60 years'}
        edu_mapping = {0: 'No formal education', 1: 'Primary education', 2: 'Secondary education', 3: 'Graduation and above'}
        for attribute, value_dict in frequencies.items(): 
            file.write(f'{attribute}\n')
            for category, count in value_dict.items():
                category = int(category) 
                if attribute == 'Sex': 
                    category_name = sex_mapping[category]
                elif attribute == "Age_category":
                    category_name = age_mapping[category]
                else:
                    category_name = edu_mapping[category]
                file.write(f"{category_name}: {count}\n")
            file.write("\n")

if __name__ == "__main__":
    # Define the file paths
    sample_data_file = 'Data.csv'
    output_file = 'Output.txt'
    
    # Read the CSV file
    sample_data = read_csv(sample_data_file)
    
    # Analyse the Sample Data
    probabilities = analyse_data(sample_data)
    
    # Generate the Synthetic Population
    synthetic_population = generate_population(probabilities, 50000)
    
    # Compute freqs
    frequencies = compute_frequencies(synthetic_population)
    
    # Write the Outputs to the .txt file
    write_to_output_file(frequencies, output_file)

print("Synthetic population saved to synthetic_population.csv")