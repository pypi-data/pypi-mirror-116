import logging
import functools
import re
import pandas as pd
import google.cloud.bigquery
from google.oauth2.service_account import Credentials
import google.cloud.bigquery.job
from google.cloud.exceptions import NotFound
from mesh.connectors.base import GoogleConnector

log = logging.getLogger(__name__)


class BqConnector(GoogleConnector):
    """
    a wee wrapper of the google client
    """
    def __init__(self, project, **kwargs):
        """
        :param optional - service_key_filename:
        :param project: a project object
        """
        super().__init__(project)
        self.scopes = (
                'https://www.googleapis.com/auth/bigquery',
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/drive'
            )
        try:
            log.debug('connecting to bq')
            self.service_key_filename = kwargs['service_key_filename']
            credentials = Credentials.from_service_account_file(
                self.service_key_filename
            ).with_scopes(self.scopes)
            self.client = google.cloud.bigquery.Client(credentials=credentials,
                                                       project=self.project)
        except KeyError as e:
            self.client = google.cloud.bigquery.Client()
            log.info('inferred from environment')


    def read_pandas_dataframe(self,  sql: str = None) -> pd.DataFrame:
        # we do not allow sql to be defined by default due to CBP approach
        log.info(f'bigquery: executing custom sql to populate pandas df: {sql[0:64]}...)')
        return self.client.query(sql).to_dataframe()


    def __get_dataset(self, dataset_id):
        try:
            dataset = self.client.get_dataset(dataset_id)
        except NotFound as e:
            dataset = google.cloud.bigquery.Dataset(f'{self.client.project}.{dataset_id}')
            dataset.location = "EU"
            dataset = self.client.create_dataset(dataset, timeout=30)
            log.info("Create: bq dataset {}.{} ".format(self.client.project, dataset.dataset_id))
        return dataset


    def write_pandas_dataframe(self, dataset: str,
                               tablename: str,
                               overwrite: bool,
                               data: pd.DataFrame):
        """
        A wrapper function that overwrites or creates a table in BigQuery from a data frame
        :param dataset: the dataset name (or database name)
        :param tablename: the table name (or collection name)
        :param overwrite: the mode being overwrite or not, this currently works with suffixes only
        :param data: the data frame containing the final feature store
        :return:
        """
        log.info('writing to {}.{}'.format(dataset, tablename))
        dataset_ref = self.__get_dataset(dataset)
        table_ref = dataset_ref.table(tablename)
        if overwrite is False:
            raise NotImplementedError('This code is presently only able to truncate/overwrite a table')
        # set up the write disposition
        jconf = google.cloud.bigquery.job.LoadJobConfig(
            write_disposition=google.cloud.bigquery.job.WriteDisposition.WRITE_TRUNCATE,
            create_disposition=google.cloud.bigquery.job.CreateDisposition.CREATE_IF_NEEDED)
        job = self.client.load_table_from_dataframe(data, table_ref, job_config=jconf)
        job.result()  # waits for query to complete


    def write_sql(self, sql:str = None) -> google.cloud.bigquery.job:
        """
        :param file_name: the name or path to the sql file to be passed in
          eg. /sql_files/fs_train.sql
        :param table_name: the name of the table that is to be created
        :param dataset: a dataset on the gcp
        :param parameters: a dictionary from the config file of specific
          paramaters to be substituted in at execution time
        :return: a dataframe
        """
        log.info(f'bigquery: executing sql to bq: {sql[0:64]}...)')
        self.client.query(sql).result()  # wait for job to finish
        return sql[0:64]


    def dry_run_sql(self, sql:str = None):
        """
        Perform a dry run of this sql against the big query api - courtesy of
        https://cloud.google.com/bigquery/docs/dry-run-queries#python
        :param sql: a complete sql string to be passed to big query
        """
        job_config = google.cloud.bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

        # Start the query, passing in the extra configuration.
        query_job = self.client.query(
            (
               sql
            ),
            job_config=job_config,
        )
        info = query_job.total_bytes_processed/1024**3
        log.info("COST: This query will process {} GiB.".format(info))
        return info


class BqConnect(BqConnector):

    """
    This doesn't make enough sense :)
    ...
    """
    def __init__(self,
                project,
                service_key_filename,
                data_type,
                dataset_name=None,
                table_name=None,
                sql=None,
                sql_file=None,
                path_conventions=None,
                overwrite=None):
        super().__init__(project=project,
                         service_key_filename=service_key_filename)
        log.debug('Bq connect args {locals()}')
        self.data_type = data_type
        self.__table_name = table_name
        self.dataset_name = dataset_name
        self.path_conventions = path_conventions
        self.overwrite = overwrite
        self.sql = sql  # this guy is operated on
        if sql_file:
            if sql:
                log.warning('you should not provide sql and a sql file... is that your intention?')
                raise ValueError("sql and sql file provided - untenable")
            with open(sql_file) as f:
                self.sql = f.read()


    def mutate_sql(self, **kwargs):
        if bool(re.search('\{.*\}', self.sql)):
            log.debug('BQ sql file requires parameterization')
            # update it to do parameterization
            self.sql = self.sql.format(
                project=self.project,
                dataset=self.dataset_name,
                table=self.table_name,
                **kwargs
            )
        return self


    def cost(self):
        """
        :return: the cost of the query in GiB
        """
        return self.dry_run_sql(self.sql)

    @property
    def read(self, **kwargs):
        """
        if kwargs are provided then handle them accordingly - the assumption at the moment
        is that the only optional 'read-time' parameters are parameters. We can make a more complex structure
        later or break out sql specific stores
        """
        return self._accessor()


    @property
    def write(self, **kwargs):
        """
        Write data to the connection. Provide kwargs to communicate directly with the
        underlying BqConnector methods
        """
        return  self._accessor(write=True)

    @property
    def table_name(self):
        if self.path_conventions:
            return f'{self.path_conventions.storage_id()}' #/{self.__table_name}' for discussion
        else:
            log.warning('no path_conventions provided')
        return self.__table_name


    @table_name.setter
    def table_name(self, table_name):
        self.__table_name = table_name


    def _accessor(self, write=False, **kwargs):
        """
        get a callable to the functions in this object that are linked to the
        data_type you would like to read and write to (e.g. gcs -> pandas and pandas -> gcs)
        :param kwargs: there to ignore all that is irrelevant
        """
        if self.data_type == 'pandas':
            if write:
                return functools.partial(self.write_pandas_dataframe,
                                        self.dataset_name,
                                        self.table_name,
                                        self.overwrite)
            f = functools.partial(self.read_pandas_dataframe, self.sql)
            return f
        if self.data_type == 'bq':
            log.warning('you are only able to write with this configuration... writing')
            return functools.partial(self.write_sql, self.sql)

        else:
            raise ValueError(f'no such datatype: "{self.data_type}"')


    
