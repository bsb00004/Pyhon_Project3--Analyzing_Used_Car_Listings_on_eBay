# Python_Project3--Pyhon_Project3-Analyzing_Used_Car_Listings_on_eBay
In this project, we worked with a dataset of used cars from eBay Kleinanzeigen, a classifieds section of the German eBay website.

The dataset was originally scraped and uploaded to Kaggle. Few modifications made from the original dataset that was uploaded to [Kaggle](https://www.kaggle.com/orgesleka/used-cars-database/data):

50,000 data points has been sampled from the full dataset, to ensure the code runs quickly. The dataset has been dirtied a bit to more, so it closely resemble what would have been expect from a scraped dataset (the version uploaded to Kaggle was cleaned to be easier to work with). The data dictionary provided with data is as follows:

- dateCrawled - When this ad was first crawled. All field-values are taken from this date.
- name - Name of the car.
- seller - Whether the seller is private or a dealer.
- offerType - The type of listing
- price - The price on the ad to sell the car.
- abtest - Whether the listing is included in an A/B test.
- vehicleType - The vehicle Type.
- yearOfRegistration - The year in which the car was first registered.
- gearbox - The transmission type.
- powerPS - The power of the car in PS.
- model - The car model name.
- kilometer - How many kilometers the car has driven.
- monthOfRegistration - The month in which the car was first registered.
- fuelType - What type of fuel the car uses.
- brand - The brand of the car.
- notRepairedDamage - If the car has a damage which is not yet repaired.
- dateCreated - The date on which the eBay listing was created.
- nrOfPictures - The number of pictures in the ad.
- postalCode - The postal code for the location of the vehicle.
- lastSeenOnline - When the crawler saw this ad last online.

The aim of this project is to clean the data and analyze the included used car listings. We will also become familiar with some of the unique benefits of Pandas .
