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

    # DataSources that aren't single use case like WebScraper need jobType variable to help map specific functionalities
        # the invoke method will be called by the pipeline



class DataSource:
    '''
    Base class used for developing DataSources that are fed into a Pipeline object.
    '''
    def __init__(self, func: function | None = None, funcArgs: tuple | dict | None = None) -> None:
        self.data = None
        self.process = self.setProcessingFunction(func)
        self.args = self.setFunctionArgs(funcArgs)
        self.kwargs = self.setFunctionKwargs(funcArgs)


    def receiveData(self, data):
        if data:
            return data
        else:
            return {}

    def setProcessingFunction(self, func):
        if func:
            return func
        else:
            None

    def setFunctionArgs(self, funcArgs):
        if type(funcArgs) is tuple:
            return funcArgs
        else:
            return None

    def setFunctionKwargs(self, funcArgs):
        if type(funcArgs) is dict:
            return funcArgs
        else:
            return None

    def invoke(self, data: dict | None):
        self.data = self.receiveData(data)
        self.process(data, *self.args, **self.kwargs)






class WebScraper(DataSource):
    def __init__(self, func: function | None = None, funcArgs: tuple | dict | None = None) -> None:
        super().__init__(func, funcArgs)
        pass

    def getreq(self, url):
        r = requests.get(url=url, 
        headers={'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36''','referer':'https://www.google.com/'})
        try:
            r.raise_for_status()
        except Exception as ex:
            logging.error(getattr(ex, 'message', repr(ex)))
        return r

    def invoke(self, data: dict | None):
        super().invoke(data)



class CallAPI(DataSource):
    def __init__(self, func: function | None = None, funcArgs: tuple | dict | None = None) -> None:
        super().__init__(func, funcArgs)
        pass

    def invoke(self, data: dict | None):
        super().invoke(data)




class BigQuery(DataSource):
#bigquery jobType should help map specific BigQuery operations
    #sql, load, insert
    def __init__(self, projectId, sqlString, jobType, func: function | None = None, funcArgs: tuple | dict | None = None) -> None:
        super().__init__(func, funcArgs)
        self.job = sqlString
        self.client = bigquery.Client(projectId)


    def run(self, client, sql):
        client(sql).result()

    def invoke(self, data: dict | None):
        super().invoke(data)
        self.run(self.client, self.job)




class CloudStorage(DataSource):
    def __init__(self, bucket, blobName, jobType, func: function | None = None, funcArgs: tuple | dict | None = None) -> None:
        super().__init__(func, funcArgs)
        pass

    def invoke(self, data: dict | None):
        super().invoke(data)




class PandasDF(DataSource):
    def __init__(self, transformations: function, func: function | None = None, funcArgs: tuple | dict | None = None) -> None:
        super().__init__(func, funcArgs)
        self.df = pd.DataFrame()
        self.transformations = transformations

    def invoke(self, data: dict | None):
        self.df = pd.DataFrame.from_dict(data)
        self.process(self.df, *self.args, **self.kwargs)







class PyDict(DataSource):
    def __init__(self, func: function | None = None, funcArgs: tuple | dict | None = None) -> None:
        super().__init__(func, funcArgs)
        

    def invoke(self, data: dict | None):
        super().invoke(data)
        










