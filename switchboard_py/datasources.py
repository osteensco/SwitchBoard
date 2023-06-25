import pandas as pd
import requests
from google.cloud import bigquery
import logging






# TODO
    # DataSources provide specific Ingestion or Transformation operations
        # data sources should essentially work like Airflow Operators
            # goal should be to make DataSources as malleable as possible
                # ex. BigQuery should take a query string as an argument, which means it can run basically any type of query job
                # f strings should be used for any dynamic generations (as opposed to something like airflow which uses jinja templating)
        # some DataSources will be for specific cloud providers, aka BigQuery, RedShift, S3, BlobStorage, etc

    # Additional DataSources:
        # WebScraper
        # CallAPI
        # BigQuery
        # CloudStorage
        # etc



class DataSource:
    '''
    Base class used for developing DataSources that are fed into a Pipeline object.
    '''
    def __init__(self) -> None:
        self.df = pd.DataFrame()










class WebScraper(DataSource):
    def __init__(self) -> None:
        super().__init__()
        pass

    def getreq(self, url):
        r = requests.get(url=url, 
        headers={'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36''','referer':'https://www.google.com/'})
        try:
            r.raise_for_status()
        except Exception as ex:
            logging.error(getattr(ex, 'message', repr(ex)))
        return r





class CallAPI(DataSource):
    def __init__(self) -> None:
        super().__init__()
        pass






class BigQuery(DataSource):
    def __init__(self, project_id, sql_string) -> None:
        super().__init__()
        self.job = sql_string
        self.client = bigquery.Client(project_id)
        self.run(self.client, self.job)

    def run(self, client, sql):
        client(sql).result()






class CloudStorage(DataSource):
    def __init__(self) -> None:
        super().__init__()
        pass



