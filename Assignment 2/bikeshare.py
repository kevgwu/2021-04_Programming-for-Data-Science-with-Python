import time as time
import pandas as pd
import numpy as np
import datetime as dt

# File names for different city inputs.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # Getting city inputs with while loop to address invalid inputs.
    i=1
    city=0
    validcities = ['chicago', 'new york city', 'washington']
    while (city not in validcities) or (i==1):
        i=0
        try:
            city = input('This program has bikeshare data for Chicago, New York City, and Washington. \n Please enter which city\'s data you\'d like to explore:')
            city = city.lower()
            if city not in validcities:
                print('Invalid Input')
        except:
            print('Invalid Input')
            continue

    # Getting month input with while loop to address invalid inputs.
    i=1
    month=0
    validmonths = ['all','january','february','march','april','may','june']
    while month not in validmonths or i==1:
        i=0
        try:
            month = input('This program has bikeshare data for months January-June. \n Please enter which month\'s data you\'d like to explore, \n if you would like to explore all months, write \'all\':')
            month = month.lower()
            if month not in validmonths:
                print('Invalid Input')
        except:
            print('Invalid Input')
            continue

    # Getting day of the week input with while loop to address invalid inputs.
    i=1
    day=0
    validdays = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    while day not in validdays or i==1:
        i=0
        try:
            day = input('This program has bikeshare data for days of the week. \n Please enter which day of the week\'s data you\'d like to explore, \n if you would like to explore all days, write \'all\':')
            day = day.lower()
            if day not in validdays:
                print('Invalid Input')
        except:
            print('Invalid Input')
            continue


    print('-'*40)
    # Returning workable inputs, which will be used in the load_data function.
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # Loading data file into DataFrame df
    df = open(CITY_DATA[city],'r')
    df = pd.read_csv(df)

    # Converting the Start Time column to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])

    # Extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['day_of_week_name'] = df['Start Time'].dt.weekday_name
    
    # Filtering by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        monthnum = [1,2,3,4,5,6]
        monthindex = dict(zip(months,monthnum))
        # filter by month to create the new dataframe
        df = df[(df['month']== monthindex[month])]

    # Filtering by day of week if applicable
    if day != 'all':
        # Filtering by day of week to create the new dataframe
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        daysnum = [6,0,1,2,3,4,5]
        dayindex = dict(zip(days,daysnum))
        df = df[(df['day_of_week']== dayindex[day])]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displaying the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month is {}'.format(popular_month))

    # Displaying the most common day of week
    popular_day = df['day_of_week_name'].mode()[0]
    print('The most common day of the week is {}'.format(popular_day))

    # Displaying the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour of the day is {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displaying most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(df['Start Station'].mode())
    print('The most commonly used start station is the station at {}'.format(popular_start_station))

    # Displaying most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is the station at {}'.format(popular_end_station))

    # Displaying most frequent combination of start station and end station trip
    CombinedStations = df['Start Station'] + '----' + df['End Station']
    popular_combination = CombinedStations.mode()[0]
    print('The most common start station-end station combination is {}'.format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    #Displaying total travel time
    t1 = pd.to_datetime(df['Start Time'])
    t2 = pd.to_datetime(df['End Time'])

    tdif =  t2.subtract(t1)
    tdifsum = tdif.sum()
    print('Total Travel Time: {}'.format(tdifsum))
    
    # Displaying mean travel time
    tmean = tdif.mean()
    print('Mean Travel Time is: {}'.format(tmean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    ucount = df['User Type'] .value_counts()
    print('Values for User Type are shown below: \n {} /n'.format(ucount))
    
    
    # Displaying counts of gender with exceptions for Washington
    try:
        gcount = df['Gender'].value_counts()
        print('Values for Gender are shown below: \n {} /n'.format(gcount))
    except:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
    
    # Displaying earliest, most recent, and most common year of birth
    try:
        earliest= int(df['Birth Year'].min())
        latest= int(df['Birth Year'].max())
        most_common= int(df['Birth Year'].mode()[0])

        print('The earliest birth year is {}, the latest birth year is {}, the most common birth year is {}'.format(earliest,latest,most_common))
    except:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    
    """
    Asks user whether they would like to display a preview (first 5 lines) of the raw data used for the stats previously provided.
    
    """
    i= 1
    raw_data_prompt=0
    acceptable_answers=['y','n','yes','no']
    
    # Prompting for an input with while loop to address invalid inputs.
    while (i==1) or (raw_data_prompt not in acceptable_answers):
        i=0
        try:
            raw_data_prompt = input('Would you like to see a preview of the raw data used for your inputs? Y or N')
            raw_data_prompt= raw_data_prompt.lower()
            if (raw_data_prompt not in acceptable_answers):
                print('Invalid Input, Please input Y or N')
                continue
        except:
            print('Invalid Input, Please input Y or N')
            continue
    # Executing display of data depending on input.
    if raw_data_prompt in ['y','yes']:
        print(df.iloc[0:5])
       
# Main function for file.   
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()