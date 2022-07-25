import pandas as pd


locations = ['St. Moritz', 'Pontresina', 'Celerina', 'Scuol', 'Menaggio', 'London', 'Prague', 'Moscow', 'Lysa nad Labem', 'Corvara in Badia', 'Brunico']
countries = ['Switzerland', 'Switzerland', 'Switzerland', 'Switzerland', 'Italy', 'United Kingdom', 'Czech Republic', 'Russian Federation', 'Czech Republic',
             'Italy', 'Italy']


def prep_df(loc, country_list):
    coord = pd.DataFrame(columns=['city_name'], data=loc)
    coord['countries'] = country_list
    return coord

print(prep_df(locations, countries))