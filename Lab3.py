import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Parameters for the Linear Congruential Generator (LCG)
initial_seed = 0  # Starting seed for the LCG
M = 101  # Multiplier
C = 1  # Increment
P = 2^32  # Modulus for the LCG

# Function to generate random numbers with LCG
def lcg(seed, M, C, P):
    new_seed = (seed * M + C) % P  # LCG formula to generate new seed
    rand_val = new_seed / P  # Normalize random value between 0 and 1
    return rand_val, new_seed

# Function to detect the cycle length in LCG
def detect_cycle(seed, M, C, P):
    visited = defaultdict(int)  # Dictionary to track unique seeds
    count = 0  # Counter for the number of generated seeds
    current_seed = seed  # Start with the given seed
    max_iterations = 10000  # Safety limit to prevent infinite loops

    # Generate random numbers until a cycle is detected
    while current_seed not in visited:
        if count > max_iterations:  # Safety break condition
            raise Exception("Loop exceeded maximum iterations. Possible infinite loop.")

        visited[current_seed] = count  # Store the seed's position
        _, current_seed = lcg(current_seed, M, C, P)  # Generate the next random number
        count += 1  # Increment the counter

    # Calculate the cycle length
    cycle_length = count - visited[current_seed]  # Difference between current count and first occurrence
    return cycle_length

# Calculate the cycle length for the given LCG parameters
cycle_length = detect_cycle(initial_seed, M, C, P)  # Calculate cycle length
print("Cycle length for LCG:", cycle_length)  # Display the cycle length

# Function to generate an array of random numbers
def generate_random_array(seed, length, M, C, P):
    random_values = []  # List to store random values
    current_seed = seed  # Initialize with the starting seed

    # Generate the specified number of random values
    for _ in range(length):
        if len(random_values) > 10000:  # Safety limit to prevent infinite loops
            raise Exception("Generated too many random numbers. Check for errors.")

        rand_val, current_seed = lcg(current_seed, M, C, P)  # Generate random number
        random_values.append(rand_val)  # Store in the list

    return random_values

# Generate an array of random numbers for visualization
random_array_length = 10000  # Desired length for the random array
random_array = generate_random_array(initial_seed, random_array_length, M, C, P)  # Generate random numbers

# Plot a histogram to visualize the distribution of random numbers
plt.figure()
plt.hist(random_array, bins=50, density=True)  # Histogram with 50 bins
plt.title("Distribution of Random Numbers (Histogram)")
plt.xlabel("Random Number")
plt.ylabel("Frequency")
plt.show()

# Generate x and y coordinates for a 2D histogram
x_vals = random_array[0::2]  # Use even indices for x values
y_vals = random_array[1::2]  # Use odd indices for y values

# Create a 2D histogram to visualize relationships between random numbers
plt.figure()
plt.hist2d(x_vals, y_vals, bins=20, cmap='viridis')  # 20 bins for each axis
plt.title("2D Histogram of Random Numbers")
plt.xlabel("X Values")
plt.ylabel("Y Values")
plt.colorbar(label="Frequency")  # Color bar for frequency
plt.show()
