#!/usr/bin/env python
# coding: utf-8

# Project : Analyzing Used Car Listings on eBay Kleinanzeigen
# In this project, we worked with a dataset of used cars from eBay Kleinanzeigen, a classifieds section of the German eBay website.

# First start importing the libraries we need and reading the dataset into pandas.

### importing libraries ###
import pandas as pd
import numpy as np

# reading CSV file, also converting the dataset into dataframe using pd(pandas) command
autos = pd.read_csv('autos.csv', encoding='Latin-1')
autos.info()
autos.head()


# Our dataset contains 20 columns, most of which are stored as strings. There are a few columns with null values, but no columns have more than ~20% null values. There are some columns that contain dates stored as strings.
# We'll start by cleaning the column names to make the data easier to work with.

### Clean Columns ####
autos.columns

# We'll make a few changes here:
# - Change the columns from camelcase to snakecase.
# - Change a few wordings to more accurately describe the columns.

autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'ab_test',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'num_photos', 'postal_code',
       'last_seen']
autos.head()

### Initial Data Exploration and Cleaning ###
# We'll start by exploring the data to find obvious areas where we can clean the data.

autos.describe(include='all')

# Our initial observations:
#  - There are a number of text columns where all (or nearly all) of the values are the same:
#     - seller
#     - offer_type
#  - The num_photos column looks odd, we'll need to investigate this further.

autos["num_photos"].value_counts()

# It looks like the num_photos column has 0 for every column. We'll drop this column, plus the other two we noted as mostly one value.

autos = autos.drop(["num_photos", "seller", "offer_type"], axis=1)

# There are two columns, price and odometer, which are numeric values with extra characters being stored as text. We'll clean and convert these.

autos["price"] = (autos["price"]
                          .str.replace("$","")
                          .str.replace(",","")
                          .astype(int)
                          )
autos["price"].head()


autos["odometer"] = (autos["odometer"]
                             .str.replace("km","")
                             .str.replace(",","")
                             .astype(int)
                             )
autos.rename({"odometer": "odometer_km"}, axis=1, inplace=True)
autos["odometer_km"].head()


### Exploring Odometer and Price ###

autos["odometer_km"].value_counts()

# We can see that the values in this field are rounded, which might indicate that sellers had to choose from pre-set options for this field. Additionally, there are more high mileage than low mileage vehicles.

print(autos["price"].unique().shape)
print(autos["price"].describe())
autos["price"].value_counts().head(20)


# Again, the prices in this column seem rounded, however given there are 2357 unique values in the column, that may just be people's tendency to round prices on the site.
# There are 1,421 cars listed with $0 price - given that this is only 2% of the of the cars, we might consider removing these rows. The maximum price is one hundred million dollars, which seems a lot, let's look at the highest prices further.

autos["price"].value_counts().sort_index(ascending=False).head(20)

autos["price"].value_counts().sort_index(ascending=True).head(20)


# There are a number of listings with prices below \$30, including about 1,500 at \$0. There are also a small number of listings with very high values, including 14 at around or over $1 million.
# Given that eBay is an auction site, there could legitimately be items where the opening bid is \$1. We will keep the \$1 items, but remove anything above \$350,000, since it seems that prices increase steadily to that number and then jump up to less realistic numbers.

autos = autos[autos["price"].between(1,351000)]
autos["price"].describe()


### Exploring the date columns ###
# There are a number of columns with date information:
# - date_crawled
# - registration_month
# - registration_year
# - ad_created
# - last_seen
# 
# These are a combination of dates that were crawled, and dates with meta-information from the crawler. The non-registration dates are stored as strings.
# We'll explore each of these columns to learn more about the listings.

autos[['date_crawled','ad_created','last_seen']][0:5]

(autos["date_crawled"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_index()
        )

(autos["date_crawled"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_values()
        )

# Looks like the site was crawled daily over roughly a one month period in March and April 2016. The distribution of listings crawled on each day is roughly uniform.

(autos["last_seen"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_index()
        )

# The crawler recorded the date it last saw any listing, which allows us to determine on what day a listing was removed, presumably because the car was sold.
# The last three days contain a disproportionate amount of 'last seen' values. Given that these are 6-10x the values from the previous days, it's unlikely that there was a massive spike in sales, and more likely that these values are to do with the crawling period ending and don't indicate car sales.

print(autos["ad_created"].str[:10].unique().shape)
(autos["ad_created"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_index()
        )

# There is a large variety of ad created dates. Most fall within 1-2 months of the listing date, but a few are quite old, with the oldest at around 9 months.

autos["registration_year"].describe()


# The year that the car was first registered will likely indicate the age of the car. Looking at this column, we note some odd values. The minimum value is 1000, long before cars were invented and the maximum is 9999, many years into the future.

### Dealing with Incorrect Registration Year Data ###

# Because a car can't be first registered before the listing was seen, any vehicle with a registration year above 2016 is definitely inaccurate. Determining the earliest valid year is more difficult. Realistically, it could be somewhere in the first few decades of the 1900s.
# One option is to remove the listings with these values. Let's determine what percentage of our data has invalid values in this column:

(~autos["registration_year"].between(1900,2016)).sum() / autos.shape[0]

# Given that this is less than 4% of our data, we will remove these rows.

# Many ways to select rows in a dataframe that fall within a value range for a column.
# Using `Series.between()` is one way.
autos = autos[autos["registration_year"].between(1900,2016)]
autos["registration_year"].value_counts(normalize=True).head(10)

# It appears that most of the vehicles were first registered in the past 20 years.

### Exploring Price by Brand ###

autos["brand"].value_counts(normalize=True)

# German manufacturers represent four out of the top five brands, almost 50% of the overall listings. Volkswagen is by far the most popular brand, with approximately double the cars for sale of the next two brands combined.
# There are lots of brands that don't have a significant percentage of listings, so we will limit our analysis to brands representing more than 5% of total listings

brand_counts = autos["brand"].value_counts(normalize=True)
common_brands = brand_counts[brand_counts > .05].index
print(common_brands)

brand_mean_prices = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    brand_mean_prices[brand] = int(mean_price)

print(brand_mean_prices)


# Of the top 5 brands, there is a distinct price gap:
# - Audi, BMW and Mercedes Benz are more expensive
# - Ford and Opel are less expensive
# - Volkswagen is in between - this may explain its popularity, it may be a 'best of 'both worlds' option.


### Exploring Mileage ##

bmp_series = pd.Series(brand_mean_prices)
pd.DataFrame(bmp_series, columns=["mean_price"])

brand_mean_mileage = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_mileage = brand_only["odometer_km"].mean()
    brand_mean_mileage[brand] = int(mean_mileage)

mean_mileage = pd.Series(brand_mean_mileage).sort_values(ascending=False)
mean_prices = pd.Series(brand_mean_prices).sort_values(ascending=False)

brand_info = pd.DataFrame(mean_mileage,columns=['mean_mileage'])
print(brand_info)
