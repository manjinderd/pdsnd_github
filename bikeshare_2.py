import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Prompts the user for city, month, and day input to filter bikeshare data.

    Returns:
        city (str): The name of the city to analyze.
        month (str): The month to filter by, or "all" for no filter.
        day (str): The day of the week to filter by, or "all" for no filter.
    """
    print("Hello! Ready to dig into some bikeshare data?")
    
    city = get_user_input("city", CITY_DATA.keys(), "Choose a city: Chicago, New York City, or Washington: ")
    month = get_user_input("month", ['january', 'february', 'march', 'april', 'may', 'june', 'all'], 
                           "Which month? January to June, or type 'all' for no month filter: ")
    day = get_user_input("day", ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'], 
                         "Which day? Monday to Sunday, or type 'all' for no day filter: ")

    print('-' * 40)
    return city, month, day

def get_user_input(input_type, valid_options, prompt_message):
    """
    Prompts the user for input and validates it.

    Args:
        input_type (str): Type of input (e.g., 'city', 'month', 'day').
        valid_options (list or set): A list or set of valid input options.
        prompt_message (str): The message to display when prompting the user.

    Returns:
        str: The validated user input.
    """
    while True:
        user_input = input(prompt_message).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid {input_type}. Please try again.")



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if needed.

    Args:
        city (str): City name.
        month (str): Month name or "all".
        day (str): Day of the week or "all".

    Returns:
        DataFrame: Filtered data.
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month
    if month != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_num]

    # Filter by day of the week
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\nChecking out the most popular times of travel...\n")
    start_time = time.time()

    # Most common month
    common_month = df['month'].mode()[0]
    print(f"Most Common Month: {common_month}")

    # Most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {common_day}")

    # Most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}")

    print(f"\nThat took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""
    print("\nNow, let's see the most popular stations and trips...\n")
    start_time = time.time()

    # Most common start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {common_start_station}")

    # Most common end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {common_end_station}")

    # Most common trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Common Trip: {common_trip[0]} to {common_trip[1]}")

    print(f"\nThis analysis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("\nEvaluating trip durations...\n")
    start_time = time.time()

    # Total travel time
    total_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_time:,} seconds")

    # Mean travel time
    mean_time = df['Trip Duration'].mean()
    print(f"Average travel time: {mean_time:.2f} seconds")

    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("\nGathering user information...\n")
    start_time = time.time()

    # User types
    user_types = df['User Type'].value_counts()
    print(f"User Types:\n{user_types}")

    # Gender counts (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"\nGender Breakdown:\n{gender_counts}")
    else:
        print("\nNo gender data available for this city.")

    # Birth year statistics (if available)
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nYear of Birth:\nEarliest: {earliest_year}\nMost Recent: {most_recent_year}\nMost Common: {common_year}")
    else:
        print("\nNo birth year data available for this city.")

    print(f"\nUser stats collected in {time.time() - start_time:.2f} seconds.")
    print('-' * 40)
    

def display_rows(df):
    """
    Displays 5 rows at a time from the DataFrame based on user input.
    
    Args:
        df (DataFrame): The DataFrame from which rows are displayed.
    """
    row_counter = 0
    total_rows = len(df)
    
    while row_counter < total_rows:
        show_rows = input("Do you want to check the first 5 rows of the dataset related to the chosen city? (yes/no): ").strip().lower()
        
        if show_rows == 'yes':
            print(df.iloc[row_counter:row_counter + 5])
            row_counter += 5
            
            while row_counter < total_rows:
                more_rows = input("Do you want to check another 5 rows of the dataset? (yes/no): ").strip().lower()
                if more_rows == 'yes':
                    print(df.iloc[row_counter:row_counter + 5])
                    row_counter += 5
                else:
                    restart_kernel = input("Do you want to restart the kernel? (yes/no): ").strip().lower()
                    if restart_kernel == 'yes':
                        return True  # Restart kernel
                    else:
                        return False  # Exit
        else:
            restart_kernel = input("Do you want to restart the kernel? (yes/no): ").strip().lower()
            if restart_kernel == 'yes':
                return True  # Restart kernel
            else:
                return False  # Exit

    # After all rows are displayed
    restart_kernel = input("You have reached the end of the dataset. Do you want to restart the kernel? (yes/no): ").strip().lower()
    if restart_kernel == 'yes':
        return True  # Restart kernel
    else:
        return False  # Exit

   

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Display the first 5 rows or more based on user input
        restart_kernel = display_rows(df)
        
        if restart_kernel:
            continue  # Restart the entire process
        else:
            # If the user doesn't want to restart the kernel, proceed with the rest of the analysis
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input("\nWould you like to restart the analysis? Type 'yes' or 'no': ").strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
