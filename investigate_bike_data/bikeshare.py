import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city =  input('Which city do you want to analyze? (Chicago, New York City or Washington.)\n').lower()
    while True:
        try:
            CITY_DATA[city]
        except:
            city = input('Sorry. You type a invaild city. You can type only one of Chicago, New York City and Washington. Please try again!\n').lower()
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Which month do you want to analyze? (from January to June, or all.)\n').lower()
    while True:
        try:
            if month == 'all':
                break
            else:
                month_list.index(month)
        except:
            month = input('Sorry, which you type is not a valid month. Please type the month from January to June, or all.\n').lower()
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ['sunday', 'monday', 'tuesday', 'wensday', 'thursday', 'friday', 'saturday']
    day = input('Which day do you want to analyze? (Sunday, Monday, ... or all.)\n').lower()
    while True:
        try:
            if day == 'all':
                break
            else:
                day_list.index(day)
        except:
            day = input('Sorry, which you type is not a valid day. Please type Sunday, Monday, ... or all.\n').lower()
        else:
            break
    print('-'*40)
    return city, month, day


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
    df =  pd.read_csv(CITY_DATA[city])
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month
    df['Day'] = pd.to_datetime(df['Start Time']).dt.weekday_name
    df['Start Hour'] =  pd.to_datetime(df['Start Time']).dt.hour
    if month != 'all':
        month = month_list.index(month) + 1
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day.lower().title()]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        common_month = month_list[df['Month'].mode()[0] - 1].title()
        print('The most common month is ' + common_month + '.')

    # TO DO: display the most common day of week
    if day == 'all':
        common_day = df['Day'].mode()[0]
        print('The most common day of week is ' + common_day + '.')

    # TO DO: display the most common start hour
    common_start_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is ' + str(common_start_hour) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is ' + common_start_station + '.')

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is ' + common_end_station + '.')

    # TO DO: display most frequent combination of start station and end station trip
    common_station_comb = df.groupby([df['Start Station'], df['End Station']]).size().idxmax()
    print('The most frequent combination of start station and end station trip is {} to {}'.format(common_station_comb[0],common_station_comb[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_day = round(df['Trip Duration'].sum()/3600/24,1)
    print('The total travel time is ' + str(total_travel_day) + ' days.')

    # TO DO: display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean()/60,1)
    print('The mean travel time is ' + str(mean_travel_time) + ' minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # TO DO: Display counts of user types
        ut_counts = len(df['User Type'].dropna(axis = 0).unique())
        print('The counts of user types is ' + str(ut_counts) + '.')

        # TO DO: Display counts of gender
        gender_counts = len(df['Gender'].dropna(axis = 0).unique())
        print('The counts of gender is ' + str(gender_counts) + '.')

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_yob = int(df['Birth Year'].min())
        recent_yob = int(df['Birth Year'].max())
        common_yob = int(df['Birth Year'].mode())
        print('The earliest, most recent, and most common year of birth are ' + str(earliest_yob) + ', ' + str(recent_yob) + ', and ' + str(common_yob) + '.')
    except:
        print('Sorry, because of missing data in {}, statistics of some dimensions did not dispay.'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
