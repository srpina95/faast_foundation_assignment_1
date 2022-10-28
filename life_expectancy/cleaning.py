# pylint: disable=line-too-long
"""import of libraries"""
import pandas as pd

def clean_data(country="PT"):
    """function which loads the eu_life_expectancy_raw and then:
        -converts it from width to long format
        -extracts the variables from the string they were in and create 4 new columns
        -extracts the float values from the value column
        -ensures the year column contains ints
    """
    eu_life_expectancy_raw = pd.read_csv\
        ("/home/srpina/faast-foundations-SRPINA/assignments/life_expectancy/data/eu_life_expectancy_raw.tsv",sep='\t')

    eu_life_expectancy_clean = \
        pd.melt(eu_life_expectancy_raw, id_vars=eu_life_expectancy_raw.columns[0], var_name="year")

    eu_life_expectancy_clean =eu_life_expectancy_clean[eu_life_expectancy_clean.columns[0]]\
        .str.split(',', expand=True)\
            .set_axis(eu_life_expectancy_clean.columns[0].split(','),axis='columns')\
                .join(eu_life_expectancy_clean)\
                    .drop(columns = eu_life_expectancy_clean.columns[0])

    eu_life_expectancy_clean["value"]= eu_life_expectancy_clean["value"]\
        .str.extract(r'(\d+.\d+)').astype('float')

    eu_life_expectancy_clean["year"]=eu_life_expectancy_clean["year"].astype("int")

    eu_life_expectancy_clean.dropna(axis=0, inplace=True)

    eu_life_expectancy_clean.rename(columns={"geo\\time": "region"}, inplace=True)

    eu_life_expectancy_clean = eu_life_expectancy_clean[eu_life_expectancy_clean["region"]==country]

    eu_life_expectancy_clean\
        .to_csv("/home/srpina/faast-foundations-SRPINA/assignments/life_expectancy/data/pt_life_expectancy.csv", index=False)
