import logging
from datasources import DataSource, Query
from utils import init_log




#TODO
    # Pipeline object should be ambiguous enough to allow various data transfer architecture patterns
        # ETL, ELT, EtLT, EL, etc
        # Similarities could be drawn between Pipeline and Airflow DAG
    # Should parallel processing of tasks be available?
    # Data should be able to be passed from one DataSource to the next when necessary
    # Pipeline object should include dry run/testing capabilities
    # Pipeline object handles logging





class Pipeline:
    def __init__(self, sources: list[DataSource]) -> None:
        self.data_objs = sources
        init_log()

    def run(self):
        data = None
        for obj in self.data_objs:
            obj.invoke(data)
            data = obj.data















