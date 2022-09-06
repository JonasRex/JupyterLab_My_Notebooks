from my_modules.kkdata import kkdata

def get_population_year(year_of_interest=2015):
    """sums up number of citizens for each age. returns dictionary with age:no_citicens"""
    neighbourhoods = kkdata.STATISTICS[year_of_interest].keys()
    age_range = set([])
    for n in neighbourhoods:
        age_range.update(kkdata.STATISTICS[year_of_interest][n].keys()) #update() on set adds any new elements

    no_citicens_per_age = {}

    for n in neighbourhoods:
        for age in age_range:
            if age in kkdata.STATISTICS[year_of_interest][n].keys():
                c_codes = set(kkdata.STATISTICS[year_of_interest][n][age].keys())
                for f_code in c_codes:
                    no_citicens_per_age.setdefault(age, 0) #sets default value if key not allready there
                    no_citicens_per_age[age] += kkdata.STATISTICS[year_of_interest][n][age][f_code]

    return no_citicens_per_age

def calculate_year_pop(data):
    pop = 0
    for key, value in data.items():
        pop += value
    return pop