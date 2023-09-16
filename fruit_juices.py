'''
Program file: fruit_juices.py

Purpose:
    i. This program estimates:
        a. the amount of produced juice (liters) from harvested fruits (kilograms)
        b. the price of produced juice taking into account processing losses

Record of revisions:
    Date        Programmer      Description of change(-s)
    ----        ----------      -------------------------
    10/9/23     Koziupa Taras   Original code
    11/9/23     Koziupa Taras   Added for loop for updating the 'juice_produced_L' dictionary values from
                                (list_of_fruits, list_of_kg_of_fruits) to (list_of_fruits, list_of_l_of_juice)
    12/9/23     Koziupa Taras   Added 'Estimating the 'Best before' date' piece of code used to calculate the date
                                up to which it's recommended to consume the juice
    12/9/23     Koziupa Taras   Added program to the Github repository. All the following commits will be available there.

Define variables:
    PRICE_PER_L -- Constant variable. Price of juice per liter, UAH;
    PROCESSING_LOSSES -- Constant variable. Processing losses of fruit mass when making juice, decimal;
    BEST_BEFORE_DAYS -- Constant variable. The number of days (from production onward) it's better to consume juice, days;
    harvested_fruits_KG -- The amount of harvested fruits, kg;
    juice_produced_L -- The amount of produced juice from fruits (losses included), liters;
    losses -- The master list of the lists of the amount of losses for each processed fruit harvested each day, decimal;
    v -- Temporary variable. Stores the values of the 'harvested_fruits_KG', later - 'juice_produced_L' dictionaries, dimensionless;
    k -- Temporary variable. Stores the keys of the 'juice_produced_L' dictionary, dimensionless;
    l -- Temporary variable. Stores the items (lists) of a master list 'losses', dimensionless;
    temp -- Temporary variable. Stores list of the amount of produced juice (including processing losses) each day, liters;
'''

# Constants
PRICE_PER_L = {
    'apple': 1,
    'pear': 0.75,
    'cherry': 1.6,
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
harvested_fruits_KG = {
    '7-24': (['apple', 'pear'], [70, 100]),
    '7-25': (['cherry', 'apricot'], [90, 50]),
    '7-26': (['apple', 'cherry'], [10, 60]),
    '7-27': (['apricot', 'pear'], [50, 70]),
}


losses = []
best_before = []
for v in harvested_fruits_KG.values():
    losses.append([PROCESSING_LOSSES.get(fruit) for fruit in v[0]])
    best_before.append([BEST_BEFORE_DAYS.get(fruit) for fruit in v[0]])

# Copying dictionary to update lists with the amount of gathered fruits (in kg) with 
# the lists of the amount produced juice (liters)
juice_produced_L = harvested_fruits_KG.copy()

for (k, v), l, bb_day in zip((juice_produced_L.items()), losses, best_before):
    # Looping through the 'juice_produced_L' dictionary and losses master list to calculate
    # the amount of produced juice taking into account processing losses for each fruit
    temp = [kg*(1 - temp_l) for kg, temp_l in zip(v[1], l)]
    
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
    
    juice_produced_L |= ({k: (v[0], temp, final_date)})

# Estimating profit from juice production (pure, w/out taking into account financial spending plan)