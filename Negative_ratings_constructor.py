import csv

def filter_csv_by_rating(input_filepath, output_filepath, target_rating=1):
    """
    Reads a CSV file, filters rows where 'Rating' equals target_rating,
    and writes these rows to a new CSV file.

    Args:
        input_filepath (str): Path to the input CSV file.
        output_filepath (str): Path where the filtered CSV file will be saved.
        target_rating (int): The rating value to filter by.
    """
    filtered_rows = []
    header = []
    rating_column_index = -1

    try:
        with open(input_filepath, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)

            # Read the header
            header = next(reader, None)
            if not header:
                print("Error: Input CSV file is empty or has no header.")
                return

            filtered_rows.append(header) # Add header to our output list

            # Try to find the 'Rating' column index
            try:
                rating_column_index = header.index('Rating')
            except ValueError:
                print(f"Error: 'Rating' column not found in the header: {header}")
                print("Please ensure your CSV has a 'Rating' column.")
                return

            # Process data rows
            rows_processed = 0
            rows_matched = 0
            for row in reader:
                rows_processed += 1
                if len(row) > rating_column_index: # Check if row has enough columns
                    try:
                        # Get rating, strip whitespace, convert to int
                        rating_value = int(row[rating_column_index].strip())
                        if rating_value == target_rating:
                            filtered_rows.append(row)
                            rows_matched += 1
                    except ValueError:
                        # Handle cases where rating is not a valid integer
                        print(f"Warning: Non-numeric rating found in row: {row}. Skipping.")
                    except IndexError:
                        # This case should be caught by len(row) > rating_column_index, but as a safeguard
                        print(f"Warning: Row with insufficient columns: {row}. Skipping.")
                else:
                    print(f"Warning: Row with insufficient columns (expected at least {rating_column_index + 1}): {row}. Skipping.")

        # Write the filtered rows to the output file
        if len(filtered_rows) > 1: # More than just the header
            with open(output_filepath, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(filtered_rows)
            print(f"Successfully processed {rows_processed} data rows.")
            print(f"Found {rows_matched} reviews with rating {target_rating}.")
            print(f"Filtered data saved to '{output_filepath}'")
        elif not header: # This case is handled above, but as a double check
            pass # Error already printed
        else:
            print(f"Successfully processed {rows_processed} data rows.")
            print(f"No reviews found with rating {target_rating} in '{input_filepath}'.")
            print(f"Output file '{output_filepath}' created with header only (or not created if header was missing).")
            # Optionally, create an empty file with header
            with open(output_filepath, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)


    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- How to use the function ---

if __name__ == "__main__":
    # Define your input and output file names
    input_csv_file = '/Users/akshaypulla/GroMo_2/gromo_play_store_reviews_detailed.csv'  # Replace with your actual input file name
    output_csv_file = './gromo_play_store_rating_1.csv'
    rating_to_filter = 1

    # Create a dummy input CSV file for testing
    # In a real scenario, you would already have this file.
   
    # Call the function
    filter_csv_by_rating(input_csv_file, output_csv_file, rating_to_filter)

    # You can also test with a different rating:
    # filter_csv_by_rating(input_csv_file, 'filtered_reviews_rating_5.csv', 5)