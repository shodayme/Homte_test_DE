import logging
import os
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.types import String, Integer
from argparse import ArgumentParser
from logger.loggerfactory import LoggerFactory


class Etl:
    def __init__(self, log_file):
        self.db_url = 'postgresql://task_user:de_task_pwd@localhost:5432/task_db'
        self.logger = LoggerFactory().get_logger('ETL_logger', log_file)

    def _read_csv_data(self, path):
        """
        Read CSV files from the specified  directory.
        """
        dataframes = []
        try:
            for file in os.listdir(path):
                with open(path + file, 'rb') as f:
                    if file.endswith('.csv'):
                        csv_df = pd.read_csv(f, delimiter=',')
                        dataframes.append(csv_df)
            df = pd.concat(dataframes, ignore_index=True)
            self.logger.info(f'Successfully loaded the CSV files under {path}.')
        except Exception as e:
            self.logger.error(f'Could not load csv files {type(e).__name__} -- {str(e)}')
        return df

    def _classify_size(self, num_employees):
        if num_employees <= 10:
            return 'Micro'
        elif 11 <= num_employees <= 50:
            return 'Small'
        elif 51 <= num_employees <= 250:
            return 'Medium'
        elif 251 <= num_employees <= 1000:
            return 'Large'
        else:
            return 'Very Large'

    def _classify_age(self, foundation_date):
        age = date.today().year - int(foundation_date)
        if age <= 20:
            return 'Emerging'
        elif 20 < age <= 40:
            return 'Established'
        else:
            return 'Legacy'

    def _format_col_names(self, name):
        return name.replace(' ', '_').lower()

    def _apply_transformations(self, df):
        try:
            df.columns = df.columns.map(self._format_col_names)
            df['maturity_level'] = df.loc[:, 'founded'].apply(lambda x: self._classify_age(x))
            df['organization_size'] = df.loc[:, 'number_of_employees'].apply(lambda x: self._classify_size(x))
            self.logger.info(f'Successfully applied transformations')
            return df
        except Exception as e:
            self.logger.error(f"Failed to apply transformations : {type(e).__name__} -- {str(e)}")

    def _build_df(self, path):
        initial_df = self._read_csv_data(path)
        return self._apply_transformations(initial_df)

    def _transform_types(self, dtype):
        if dtype == 'int64':
            return Integer
        elif dtype == 'object':
            return String

    def write_to_db(self, path):
        df = self._build_df(path)
        try:
            dtypes = {col: self._transform_types(dtype.name) for col, dtype in df.dtypes.items()}
            self.logger.info(f'Writing transformed data to database ...: {dtypes}')
            engine = create_engine(self.db_url)
            df.to_sql('organizations', engine, if_exists='append', index=True, index_label='id', dtype=dtypes)
            self.logger.info(f'Data written to database')
        except Exception as e:
            self.logger.error(f'Failed to write transformed data to database : {type(e).__name__} -- {str(e)}')


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--data_path', required=True, default=False,
                        help='absolute path to the directory containing CSV files')
    parser.add_argument('-l', '--log_file', required=False, default='./logs/etl_logs.log',
                        help=f'absolute path to the logs path. Defaults to  ./logs/etl_logs.log')
    args = parser.parse_args()
    etl = Etl(args.log_file)
    etl.write_to_db(args.data_path)


if __name__ == '__main__':
    main()
