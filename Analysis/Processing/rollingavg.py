import pandas as pd

# Read in the CSV file
data = pd.read_csv("Readings/ASRT/06-02-2023 (ECE Lab)/power_19:37:50.csv")

# Calculate the rolling average
rolling_avg = data.iloc[:, 1].rolling(window=5, center=True).mean()

# Add the rolling average as a new column in the dataframe
data["Rolling Average"] = rolling_avg

# Write the updated data to a new CSV file
data.to_csv("Readings/ASRT/06-02-2023 (ECE Lab)/power_processed_19:37:50.csv", index=False)
