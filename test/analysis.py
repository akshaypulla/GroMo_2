import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os # Added for directory creation

# --- Data defined directly as Python lists ---
year_month_data = [
    "2025-05", "2025-04", "2025-03", "2025-02", "2025-01",
    "2024-12", "2024-11", "2024-10", "2024-09", "2024-08", "2024-07", "2024-06", "2024-05", "2024-04", "2024-03", "2024-02", "2024-01",
    "2023-12", "2023-11", "2023-10", "2023-09", "2023-08", "2023-07", "2023-06", "2023-05", "2023-04", "2023-03", "2023-02", "2023-01",
    "2022-12", "2022-11", "2022-10", "2022-09", "2022-08", "2022-07", "2022-06", "2022-05", "2022-04", "2022-03", "2022-02", "2022-01",
    "2021-12", "2021-11", "2021-10", "2021-09", "2021-08", "2021-03", "2021-02", "2021-01",
    "2020-12", "2020-10", "2020-08", "2020-07", "2020-06", "2020-03", "2020-01",
    "2019-12", "2019-11", "2019-10", "2019-08"
]

payout_issues_data = [
    9, 20, 14, 11, 11, 16, 17, 19, 12, 18, 12, 18, 15, 10, 16, 14, 10,
    17, 18, 16, 14, 13, 15, 20, 16, 13, 18, 15, 12,
    18, 20, 15, 14, 16, 17, 22, 25, 18, 15, 14, 16,
    19, 10, 3, 1, 1, 3, 1, 1,
    1, 0, 1, 3, 1, 1, 3,
    1, 1, 0, 1
]

lead_tracking_data = [
    5, 9, 5, 4, 4, 8, 9, 8, 6, 7, 5, 8, 6, 5, 7, 6, 5,
    9, 8, 8, 7, 6, 7, 9, 7, 6, 8, 7, 6,
    9, 10, 7, 7, 8, 8, 11, 12, 9, 7, 7, 8,
    10, 5, 2, 1, 0, 0, 0, 0,
    0, 0, 1, 1, 0, 1, 1,
    1, 0, 0, 1
]

poor_customer_support_data = [
    6, 8, 6, 4, 4, 6, 7, 5, 5, 6, 4, 6, 5, 4, 6, 5, 3,
    7, 7, 6, 5, 5, 6, 8, 6, 5, 7, 6, 5,
    8, 9, 6, 6, 7, 7, 10, 11, 8, 6, 6, 7,
    9, 4, 2, 1, 1, 2, 0, 1,
    1, 1, 1, 2, 0, 0, 2,
    0, 0, 0, 0
]

fraud_scam_data = [
    12, 23, 15, 10, 10, 15, 18, 19, 12, 17, 10, 16, 14, 9, 14, 12, 9,
    15, 16, 14, 13, 11, 12, 17, 13, 11, 15, 12, 10,
    15, 17, 12, 11, 13, 14, 18, 20, 15, 12, 11, 13,
    16, 8, 2, 1, 0, 1, 0, 0,
    1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0
]

hidden_charges_data = [
    4, 9, 6, 6, 5, 7, 8, 7, 3, 3, 1, 2, 3, 2, 3, 3, 2,
    4, 3, 3, 2, 2, 2, 2, 3, 2, 2, 2, 1,
    2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0
]

app_performance_data = [
    2, 2, 1, 2, 3, 3, 4, 4, 3, 3, 1, 3, 2, 1, 2, 1, 2,
    4, 5, 3, 2, 2, 2, 4, 2, 1, 3, 2, 2,
    4, 5, 3, 3, 4, 3, 5, 6, 4, 3, 3, 4,
    5, 3, 1, 0, 0, 0, 0, 0,
    1, 0, 1, 1, 1, 0, 1,
    0, 0, 0, 0
]

account_blocking_data = [
    1, 2, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0,
    1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0
]

misleading_tc_data = [
    3, 4, 4, 2, 2, 4, 5, 5, 2, 3, 2, 3, 3, 2, 3, 2, 2,
    3, 4, 3, 3, 2, 3, 4, 3, 2, 4, 3, 2,
    3, 4, 3, 3, 3, 3, 5, 5, 4, 3, 3, 3,
    4, 2, 1, 0, 0, 1, 0, 0,
    0, 0, 0, 1, 0, 0, 1,
    0, 0, 0, 0
]

data_privacy_concerns_data = [
    0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0
]

# --- Create the dictionary for the DataFrame ---
data_for_df = {
    'Year-Month': year_month_data,
    "Payout Issues (Not Rec'd/Delayed)": payout_issues_data,
    "Lead Tracking & Status Issues": lead_tracking_data,
    "Poor Customer Support": poor_customer_support_data,
    "Accusations of Fraud/Scam": fraud_scam_data,
    "Hidden/High Charges & Fees": hidden_charges_data,
    "App Performance & Technical Issues": app_performance_data,
    "Account Blocking/Deactivation": account_blocking_data,
    "Misleading T&Cs/Promises": misleading_tc_data,
    "Data Privacy Concerns": data_privacy_concerns_data
}

# --- Create DataFrame ---
df = pd.DataFrame(data_for_df)

# Convert 'Year-Month' to datetime objects
df['Year-Month'] = pd.to_datetime(df['Year-Month'], format='%Y-%m')

# Set 'Year-Month' as index
df = df.set_index('Year-Month')

# Sort by date (important for time series plots)
df = df.sort_index()

# --- Define directory for saving graphs ---
output_dir = "review_problem_graphs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# List of problem columns to plot
problem_columns = [
    "Payout Issues (Not Rec'd/Delayed)",
    "Lead Tracking & Status Issues",
    "Poor Customer Support",
    "Accusations of Fraud/Scam",
    "Hidden/High Charges & Fees",
    "App Performance & Technical Issues",
    "Account Blocking/Deactivation",
    "Misleading T&Cs/Promises",
    "Data Privacy Concerns"
]

# --- Generate and save a plot for each problem column ---
for column in problem_columns:
    fig, ax = plt.subplots(figsize=(14, 7)) # Get figure and axes objects
    ax.plot(df.index, df[column], marker='o', linestyle='-', label=column)

    # Formatting the x-axis to show year and month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    num_data_points = len(df.index)
    if num_data_points <= 12:
        tick_interval = 1
    elif num_data_points <= 36:
        tick_interval = 3
    elif num_data_points <= 60:
        tick_interval = 6
    else:
        tick_interval = 12

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=max(1, tick_interval)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())

    ax.set_title(f'Frequency of "{column}" Over Time', fontsize=16)
    ax.set_xlabel('Year-Month', fontsize=12)
    ax.set_ylabel('Number of Mentions', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    ax.legend(loc='upper left')
    ax.grid(True, which='major', linestyle='--', linewidth=0.7)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.4)

    plt.tight_layout()

    # --- Sanitize filename and Save the plot ---
    # Replace characters not suitable for filenames
    safe_column_name = column.replace(' ', '_').replace('/', '_').replace("'", "").replace('(', '').replace(')', '').replace('&', 'and')
    filename = os.path.join(output_dir, f"{safe_column_name}_trend.png")
    plt.savefig(filename, dpi=300) # dpi for higher resolution
    print(f"Saved graph: {filename}")

    plt.close(fig) # Close the figure to free memory

print("\nAll graphs have been saved.")