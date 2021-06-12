import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def greet_user():
    print("    (\_/)            \n    (O.o) ----> Hi ! I'm Bicycle Bunny.")
    print("    (> <))      What is your name?")
    user_name = input()
    print(f'\n{user_name}, do you want to see some bike data?\n')
    x = input("'y' to continue\nEnter to exit.\n")
    if x.casefold() == 'y':
        print('\n    __o  \n    \<_ \n (_)/(_)')
        time.sleep(0.5)
        print('\n       __o  \n       \<_ \n    (_)/(_)')
        time.sleep(0.5)
        print('\n             __o  \n             \<_ \n          (_)/(_)')
        time.sleep(0.5)
        print('\n                   ~~O\n                 -  /\,\n                -  -|~(*)\n               -  (*)')
        print(' '*17 + 'lets go!')
        time.sleep(0.5)
    else:
        exit()
    return user_name


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #define the input options
    city, month, day = 0, 7, ''
    week_day = ['All', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    city_list = ['Chicago', 'New York City', 'Washington']
    month_list = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    # get user input for city (chicago, new york city, washington).
    while True: #Use while loop to catch values out of range
        try:
            city = int(input('\nSelect a CITY by typing the associated number.\n1 for Chicago\n2 for New York City\n3 for Washington\n\n'))
        except ValueError:
            print('')
        if city not in range(1,4):
            print(f"\nThe value entered is not in range.\nPlease enter a number '1', '2', or '3'")
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True: #Use while loop to catch ValueError and values out of range
        try:
            month = int(input('\nSelect a MONTH by entering the associated number.\n0 for All\n1 for January\n...\n5 for May\n6 for June\n\n'))
        except ValueError:
            print('Please enter a number only')
        if month not in range(0,7):
            print(f'\nThe value entered is not in range.\nPlease enter a number from 0 to 6')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nSelect week DAY/s: ' + ', '.join(week_day) + '\n').title()
    # check that value entered is valid
    while day not in week_day:
        day = input('Reselect a day from options: ' + ', '.join(week_day) + '\n').title()
    else:
        city, month = city_list[city-1], month_list[month]
        print(f'\nYou have selected\nCity:     {city}\nMonth/s:  {month}\nDay/s:    {day}')

    print('-'*40)
    return city, month, day


def display_rawdata(city):
    """
    Display the datatframe loaded 5 rows at a time and
    allow the user to scroll 5 lines at a time untill exit.
    """
    start_time = time.time()
    df = pd.read_csv(CITY_DATA[city.casefold()])
    i_row = 0
    count_notna, count_null = df.notna().sum().sum(), df.isna().sum().sum()
    u_input = 'y'
    # https://stackoverflow.com/questions/11707586/how-do-i-expand-the-output-display-to-see-more-columns-of-a-pandas-dataframe
    # increase the number of columns printed in terminal window to match data
    pd.set_option('display.max_columns', df.shape[1])
    print(f'\nPlease note!\nThe data for {city.title()} has: \n{df.shape[1]} categories (columns) and {df.shape[0]} trips (rows)')
    print(f'{count_null} missing values or {round(count_null/(count_null + count_notna)*100,2)} % NaN/Null')
    print(f'The dataframe size is {round(df.memory_usage(index=True).sum()/1000/1000,3)} Megabyte\n')
    print('*'*55)
    print(f'Table will be wrapped and continue on the next line')
    print('*'*55)
    input('\nPress Enter key to continue.\n')
    while u_input == 'y':
        print(df.iloc[i_row:(i_row+5),:])
        i_row += 5
        u_input = input("'y' to continue, Enter to close raw data view. \n")
        if u_input != 'y':
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


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
    #Load raw data file
    df = pd.read_csv(CITY_DATA[city.casefold()])
    #Convert the 'Start Time' to DateTime and extract month and day to new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    #Use the given month and day input to filter the dataframe
    if month.casefold() != 'all':
        df = df[df['Month'] == month]
    if day.casefold() != 'all':
        df = df[df['Day'].str.startswith(day)]

    return df


def time_stats(df):
    """Filter data based on user inputs and
    display statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # start with blank series
    month_count, day_count, hour_count, = pd.Series(dtype=object), pd.Series(dtype=object), pd.Series(dtype=object)
    # filter DataFrame based on user inputs

    print('The most frequent travel times')
    # display the most common month
    # check if the DataFrame has been filtered by month
    if (df['Month'].unique().size) > 1:
        month_count = df['Month'].value_counts()
        print(f'month:  {month_count.index[0]}   ({month_count[0]} trips)')
    else:
        print('month filter "' + df['Month'].unique()[0] + '" applied.')

    # display the most common day of week
    # check if the DataFrame has been filtered by week day
    if (df['Day'].unique().size) > 1:
        day_count = df['Day'].value_counts()
        print(f'day:    {day_count.index[0]}   ({day_count[0]} trips)')
    else:
        print('day filter "' + df['Day'].unique()[0] + '" applied.')

    # display the most common start hour
    # create a new column with start hour
    df['Strt_hour'] = df['Start Time'].dt.hour
    hour_count = df['Strt_hour'].value_counts()
    print(f'hour:   {hour_count.index[0]} (24 hr/day)   ({hour_count[hour_count.index[0]]} trips)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Input:
        df - DataFrame imported from csv.
    Parameters:
        df_gender - If gender data is available,
        a DataFrame to store duration per gender.
    Output:
        Displays statistics on the total and average trip duration.
        Displays statistics per gender if gender data is available.
    """
    trp_mean, trp_total = 0,0

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # create a new column with duration as time type
    df['TimeDelta'] = pd.to_timedelta(df['Trip Duration'],unit='s')
    # calculate total and avg. triptime
    trp_mean = str(df['TimeDelta'].mean())
    trp_total = str(df['TimeDelta'].sum())
    # display total and avg. trip time and remove ns
    print(f'Average: {trp_mean.split(".")[0]}\nTotal:   {trp_total.split(".")[0]}')
    # check if the DataFrame has gender data
    if 'Gender' in df.columns.values:
        # creat a dictionary with the min, mean and max per gender
        dic_gender = {'min_s' : df.groupby(['Gender'])['Trip Duration'].min(),
                      'mean_s' : round(df.groupby(['Gender'])['Trip Duration'].mean(),ndigits=1),
                      'max_s' : df.groupby(['Gender'])['Trip Duration'].max()}
        # create a DataFrame from the dictionary
        df_gender = pd.DataFrame(dic_gender)
        # create new colums with time data format
        df_gender['min'] = pd.to_timedelta(df_gender['min_s'],unit='s').astype(str)
        df_gender['mean'] = pd.to_timedelta(df_gender['mean_s'],unit='s').astype(str)
        df_gender['max'] = pd.to_timedelta(df_gender['max_s'],unit='s').astype(str)
        # format the DataFrame for display and remove ns from mean
        # code can be simplified by using for loop to iterate throug DataFrame
        df_gender.at['Female','mean'] = df_gender.at['Female','mean'].split('.')[0]
        df_gender.at['Male','mean'] = df_gender.at['Male','mean'].split('.')[0]
        df_gender = df_gender.drop(['min_s', 'mean_s','max_s'], axis = 1).T
        # print the duration statistics by gender
        print(f'\nTrip time per gender\n{df_gender}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    min, mode, max = 0,0,0
    t = time.localtime()

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # rename the unique id column label
    df = df.rename(columns = {'Unnamed: 0': 'Trip ID'})
    #check if the city has gender data
    if 'Gender' in df.columns.values:
        #fill all the null/NaN values to get correct counts for 'Gender'
        df['Gender'] = df['Gender'].fillna('Null')
        # calculate counts per gender
        count_gender = df.groupby(['Gender'])['Trip ID'].count()
        # Display counts of gender
        print(f'Count by {count_gender}\n')
    else:
        print('The city has no gender data\n')

    #fill all the null/NaN values to get correct counts for 'User Type'
    df['User Type'] = df['User Type'].fillna('Null')
    # calculate counts per user type
    count_utype = df.groupby(['User Type'])['Trip ID'].count()
    # Display counts of user types
    print(f'Count by {count_utype}\n')

    #check if the city has birth year data
    if 'Birth Year' in df.columns.values:
        # Display earliest, most recent, and most common year of birth
        min, mode, max = int(df['Birth Year'].min()), int(df['Birth Year'].mode()), int(df['Birth Year'].max())
        print('Year of birth:')
        print(f'Earliest:    {min}  (age: {int(time.strftime("%Y", t)) - min})')
        print(f'Most common: {mode}  (age: {int(time.strftime("%Y", t)) - mode})')
        print(f'Most recent: {max}  (age: {int(time.strftime("%Y", t)) - max})')
    else:
        print('The city has no birth year data\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Station Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most commonly used START station: {df['Start Station'].mode()[0]}")
    # display most commonly used end station
    print(f"Most commonly used END station:   {df['End Station'].mode()[0]}")
    # display most frequent combination of start station and end station trip
    # create new column to join start - end pair
    df['Start-End'] = df['Start Station'] + " to " + df['End Station']
    #print(df[['Start Station','End Station','Start-End']].head(5)) #dataframe[column][row]
    print(f"Most frequent combination of start station and end station:\n'{df['Start-End'].value_counts().index[0]}' with {df['Start-End'].value_counts()[0]} trips.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    user_name = greet_user()
    while True:
        city, month, day = get_filters()

        print(f'\nDo you want to take a peek at the raw data for {city} first?')
        if input("'y' to continue \nEnter to skip\n").casefold() == "y":
            display_rawdata(city)

        df = load_data(city, month, day)

        print('\nDo you want to see info on most Frequent Times of Travel?')
        if input("'y' to continue \nEnter to skip\n").casefold() == "y":
            time_stats(df)
        print('\nDo you want to see info on trip Duration?')
        if input("'y' to continue \nEnter to skip\n").casefold() == "y":
            trip_duration_stats(df)
        print('\nDo you want to see info on Users?')
        if input("'y' to continue \nEnter to skip\n").casefold() == "y":
            user_stats(df)
        print('\nDo you want to see info on Stations?')
        if input("'y' to continue \nEnter to skip\n").casefold() == "y":
            station_stats(df)
        print('\n          __o  \nEnd of    \<_   data\n       (_)/(_)\n')
        restart = input(f"\n{user_name}, would you like to restart? \n'y' to continue \nEnter to exit.\n")
        if restart.casefold() != 'y':
            break


if __name__ == "__main__":
	main()
