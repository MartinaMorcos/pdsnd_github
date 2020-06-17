import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York, or Washington?").title()
    while city not in ("Chicago","New York","Washington"):
        city = input("The city name you entered is not available. Please enter Chicago, New York, or Washington: ").title()
    
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    month_or_day = input("Would you like to filter the data by month, day, or not at all? Type ""all"" for no time filter: ").title()
    while month_or_day not in ("Month","Day","All"):
        month_or_day = input("Please enter month, day or all to filter data accordingly: ").title()

    # get user input for month (all, january, february, ... , june)
    if month_or_day == 'Month':
        month = input("Which month? January, February,.....,June: ").title()
        while month not in months:
            month = input("Please enter a valid month between january and june: ").title()
        day = "All"
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif month_or_day =='Day':
        day = input("Which day? Monday, Tuesday, ....Sunday: ").title()
        while day not in days:
            day = input("Please enter a valid day between monday and sunday: ").title()
        month = "All"
    elif month_or_day == "All":
        month = "All"
        day = "All"

    

    print('*'*40)
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
    city= city.lower()
    month = month.lower()
    day = day.lower()
        # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_comm_month = df["Start Time"].dt.month.mode()[0]
    print("Most common month is {}".format(most_comm_month))
    
    # display the most common day of week
    most_comm_day = df["Start Time"].dt.day_name().mode()[0]
    print("Most common day is {}".format(most_comm_day))
    
    # display the most common start hour
    most_comm_hour = df["Start Time"].dt.hour.mode()[0]
    print("Most common hour is {}".format(most_comm_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_comm_start = df["Start Station"].mode()[0]
    print("Most common Start Station is {}".format(most_comm_start))

    # display most commonly used end station
    most_comm_end = df["End Station"].mode()[0]
    print("Most common End Station is {}".format(most_comm_end))

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most frequent combination of start station and end station is {} and {}".format(combination[0],combination[1]))
  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
 
    #travel_time = (df["End Time"]-df["Start Time"])/np.timedelta64(1,'m')
    travel_time = (df["End Time"]-df["Start Time"]).sum()
    print("The total travel time is {} ".format(travel_time))

    # display mean travel time
    mean_time = (df["End Time"]-df["Start Time"]).mean()
    print("The mean travel time is {} minutes ".format(mean_time/np.timedelta64(1,'m')))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_counts = df["User Type"].value_counts()
    print("The count of user types is \n{} \n".format(user_counts))



    if(set(["Gender","Birth year"]).issubset(df.columns)):
        # Display counts of gender
        gender_counts = df["Gender"].value_counts()
        print("The gender count is \n{} \n".format(gender_counts))


        # Display earliest, most recent, and most common year of birth
        print("Earliest year of birth is {} ".format(df["Birth Year"].min()))
        print("Most recent year of birth is {} ".format(df["Birth Year"].max()))
        print("Most common year of birth is {} ".format(df["Birth Year"].mode()[0]))
    else:
        print("The dataset for washington has no fields for gender and Birth year\n")
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        N=len(df)
        n=0
        print(N)

        raw_data = input('\nDo you want to see the raw data? Enter yer or no.\n')
        while raw_data.lower() not in ("yes","no"):
            raw_data = input('\nPlease enter yes or no only. Do you want to see the raw data?\n')
        while n<N:
            if raw_data.lower() != 'yes':
                break
            else:
                print(df[n:n+5])
                raw_data = input('\nDo you want to see the next 5 rows? Enter yer or no.\n')
                while raw_data.lower() not in ("yes","no"):
                    raw_data = input('\nPlease enter yes or no only. Do you want to see the raw data?\n')
                n+=5



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in ('yes','no'):
            restart = input('\nPlease enter yes or no only. Would you like to restart?\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
