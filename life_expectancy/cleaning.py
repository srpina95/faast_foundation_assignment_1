# pylint: disable=line-too-long
"""import of libraries"""
from pathlib import Path
import argparse
import pandas as pd

current_filepath = Path(__file__).parent.resolve()


def clean_data(country="PT"):
    """function which loads the eu_life_expectancy_raw and then:
        -converts it from width to long format
        -extracts the variables from the string they were in and create 4 new columns
        -extracts the float values from the value column
        -ensures the year column contains ints
    """
    eu_life_expectancy_raw = pd.read_csv(current_filepath / "data" / "eu_life_expectancy_raw.tsv",sep='\t')

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

    eu_life_expectancy_clean.to_csv(current_filepath /"data" / "pt_life_expectancy.csv", index=False)


if __name__=="__main__": # pragma: no cover
    parser = argparse.ArgumentParser(description='main function for your library')
    parser.add_argument('--country',
                        type=str,
                        required=False,
                        default="PT",
                        help='country code on which to focus')
    args = parser.parse_args()

    clean_data(args.country)
