# refactoring edits
import time
import pandas as pd
import numpy as np

# refactoring data dictionary
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_txt2num = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
day_txt2num = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter the city: (chicago, new york city, washington)').lower()
    while city not in CITY_DATA:
        print("The city you entered is invalid!")
        city = input('Please re-enter the city: ').lower()

    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # get user input for month (all, january, february, ... , june)
    month = input("Please enter the month (january, february, ... , june), or you can write 'all' if you want the stats for all the months: ").lower()
    while month not in valid_months:
        print("The month you entered is invalid!")
        month = input('Please re-enter the month: ').lower()

    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the day of week (monday, tuesday, ... sunday) or you can write 'all' if you want the stats for all the days of week: ").lower()
    while day not in valid_days:
        print("The day of week you entered is invalid!")
        day = input('Please re-enter the day of week: ').lower() 

    print('-'*40)
    return city, month, day


# We are making an assumption that the starting month and ending month do not span across two months
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df = df.drop(df.columns[0], axis=1)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['end Time'] = pd.to_datetime(df['End Time'])

        
    df_filtered = df.copy()
    if month != 'all':
        month = months_txt2num[month]   # convert it to a number
        df_filtered = df[df['Start Time'].dt.month==month]
    
    if day != 'all':
        day = day_txt2num[day]  #convert it to a number
        df_filtered = df_filtered[df_filtered['Start Time'].dt.dayofweek==day]


    return df_filtered


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    number_month = df['Start Time'].dt.month.value_counts().head(1).index[0]

    freq_month = month_dict[number_month]
    print(f'The most common month is {freq_month}')

    # display the most common day of week
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    common_day_num = df['Start Time'].dt.dayofweek.value_counts().head(1).index[0]
    common_day = day_dict[common_day_num]

    # display the most common start hour
    print(f'The most common day of week is {common_day}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().head(1).index[0]
    print(f'The most common start station is {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().head(1).index[0]
    print(f'The most common end station is {common_end_station}')

    # display most frequent combination of start station and end station trip
    common_combination_station = df.groupby(by=['Start Station', 'End Station']).size().sort_values(ascending=False).head(1).index[0] 
    print(f'The most common combination of start station and end station is {common_combination_station}') 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_secs = df['Trip Duration'].sum()
    hours = int(total_secs//60//60)
    minutes = int((total_secs - hours*60*60)//60)
    seconds = total_secs - hours*60*60 - minutes*60

    print(f'Total travel time is {hours} hours, {minutes} minutes, and {seconds} seconds')

    # display mean travel time
    mean_total_sec = df['Trip Duration'].mean()
    minutes = int(mean_total_sec//60)
    seconds = mean_total_sec - minutes*60
    print(f'The mean travel time is {minutes} minutes and {seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Displaying the counts for user types:')
    print(user_types)

    # writing conditions for the washington data that doesn't have gender and birth year columns
    if 'Gender' in df.columns:
        # Display counts of gender
        gender_types = df['Gender'].value_counts()
        print('-'*40)
        print('Displaying the counts for gender:')        
        print(gender_types)  

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        birth_year_earliest = int(df['Birth Year'].min())
        birth_year_recent = int(df['Birth Year'].max())
        birth_year_common = int(df['Birth Year'].value_counts().head(1).index[0])
        print('-'*40)
        print('Displaying the stats for year of birth:')
        print(f'The earliest birth year is {birth_year_earliest}')
        print(f'The most recent birth year is {birth_year_recent}')
        print(f'The most common birth year is {birth_year_common}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df.head()

        # Display the statistics to the user
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display 5 rows of data at a time if the user specifies that they would like to
        row = 0
        view_data = input('\nWould you like to view 5 rows of individual trip data? (yes/no)\n')
        while view_data.lower() == 'yes':
            print(df.iloc[row:row+5])
            row += 5
            view_data = input('Do you wish to continue?: ').lower()


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


