import csv

'''
Program file: fruit_juices.py

Purpose:
    i. This program estimates:
        a. the amount of produced juice (liters) from harvested fruits (kilograms)
        b. the price of produced juice taking into account processing losses
    ii. Creates and fills in the .csv file that stores information about harvesting date,
kind of fruits harvested, amount of juice produced, 'best before' date and price at which
those juices are being sold.

Record of revisions:
    Date        Programmer      Description of change(-s)
    ----        ----------      -------------------------
    10/9/23     Koziupa Taras   Original code
    11/9/23     Koziupa Taras   Added for loop for updating the 'juice_produced_L' dictionary values from
                                (list_of_fruits, list_of_kg_of_fruits) to (list_of_fruits, list_of_l_of_juice)
    12/9/23     Koziupa Taras   Added 'Estimating the 'Best before' date' piece of code used to calculate the date
                                up to which it's recommended to consume the juice
    16/9/23     Koziupa Taras   Added program to the Github repository. All the following commits will be available there.
    25/10/23    Koziupa Taras   Added function of writing the data to the .csv database file. Final improvements

Define variables:
    PRICE_PER_L -- Constant variable. Price of juice per liter, UAH;
    PROCESSING_LOSSES -- Constant variable. Processing losses of fruit mass when making juice, decimal;
    BEST_BEFORE_DAYS -- Constant variable. The number of days (from production onward) it's better to consume juice, days;
    harvested_fruits -- The amount of harvested fruits, kg;
    juice_produced -- The amount of produced juice from fruits (losses included), liters;
    losses -- The master list of the lists of the amount of losses for each processed fruit harvested each day, decimal;
    v -- Stores the values of the 'harvested_fruits', later - 'juice_produced_L' dictionaries, dimensionless;
    k -- Stores the keys of the 'juice_produced_L' dictionary, dimensionless;
    l -- Stores the items (lists) of a master list 'losses', dimensionless;
    temp_liters -- Stores list of the amount of produced juice (including processing losses) each day, liters;
    bb_day -- The number of days it's recommended to consume the juice, days;
    temp_profit -- List that stores the amount of money obtained for selling each portion of juice, $$;
    month -- Month part of the 'Best before' date, months;
    day -- Day part of the 'Best before' date, days;
    full_months -- The number of full months of the 'Best before' date, months;
    days_left -- The number of (remaining) days should be added to the 'full_months' variable, days;
    b -- Stores the 'Best before' day for a given juice produced, day;
    f_m -- Stores the number of full months to the 'Best before' date for a given juice produced, months;
    final_date -- Calculated final date of recommeneded consumption of the juice, dimensionless;
    d_l -- Used to calculate the precise 'Best before' date, dimensionless;
    fields -- Headers of the .csv file, dimensionless;
    csvfile -- Opened .csv file in 'writing' mode, dimensionless;
    csvwriter -- A .csv writer object, dimensionless;
    iterator -- Stores the length of the harvested_fruits[0] portion of dectionary, dimensionless;
    info_row -- Information row for the .csv file that stores an information about produced juices, dimensionless.
'''

# Constants
PRICE_PER_L = {
    'apple': 0.75,
    'pear': 1,
    'cherry': 2.3,
    'apricot': 1.5
}
PROCESSING_LOSSES = {
    'apple': 0.1,
    'pear': 0.05,
    'cherry': 0.25,
    'apricot': 0.2
}
BEST_BEFORE_DAYS = {
    'apple': 35,
    'pear': 20,
    'cherry': 60,
    'apricot': 30
}

# Given data
harvested_fruits = {
    '7-24': (['apple', 'pear'], [70, 100]),
    '7-25': (['cherry', 'apricot'], [90, 50]),
    '7-26': (['apple', 'cherry'], [10, 60]),
    '7-27': (['apricot', 'pear'], [50, 70]),
}


losses = []
best_before = []
for v in harvested_fruits.values():
    losses.append([PROCESSING_LOSSES.get(fruit) for fruit in v[0]])
    best_before.append([BEST_BEFORE_DAYS.get(fruit) for fruit in v[0]])

# Copying dictionary to update lists with the amount of gathered fruits (in kg) with 
# the lists of the amount of produced juice (liters)
juice_produced = harvested_fruits.copy()

for (k, v), l, bb_day in zip((juice_produced.items()), losses, best_before):
    # Looping through the 'juice_produced' dictionary and losses master list to calculate
    # the amount of produced juice taking into account processing losses for each fruit
    temp_liters = [kg*(1 - temp_l) for kg, temp_l in zip(v[1], l)]
    
    # Estimating profit from juice production (pure, w/out taking into account financial spending plan)
    temp_profit = [round(PRICE_PER_L.get(fruit)*liters, 2) for fruit,liters in zip(v[0], temp_liters)]
    
    # Estimating the 'Best before' date
    month = int(k[:k.find('-')])
    day = int(k[k.find('-')+1:])

    full_months = [b//30 for b in bb_day]
    days_left = [b - (f_m*30) for b, f_m in zip(bb_day, full_months)]
    final_date = []
    for d_l, f_m in zip(days_left, full_months):
        if d_l + day < 30: day_str = str(d_l + day)
        else:
            day_str = str(d_l - (30-day))
            month += 1
        month += f_m
        final_date.append(str(month) + '-' + day_str)
    
    juice_produced |= ({k: (v[0], temp_liters, final_date, temp_profit)})

print(juice_produced)

# Writing all the data to .csv file
fields = ['Date', 'Fruit', 'Produced, l', "'Best before' date", 'Profit, $']

with open('juice_production_unit.csv', 'w', newline='') as csvfile:
    # Creating a .csv writer object
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    
    for k, v in juice_produced.items():
        # Wrinting in the date field
        csvwriter.writerow([k])
        
        # Inner loop for gathering information about produced juices
        for iterator in range(len(best_before[0])):
            info_row = [info[iterator] for info in v]
            # Wrinting in the information field
            csvwriter.writerow([''] + info_row)