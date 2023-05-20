import boto3
import time


class Athena(object):
    def __init__(self):
        self.athena = boto3.client("athena")
        self.s3 = boto3.resource("s3")
        self.result_output_location = "s3://athena-query-location-731776214881/"
        self.bucket_name = "athena-query-location-731776214881"

    def get_sql_results(self, query: str, timeout_in_seconds: int) -> bytes:
        """
        Executes a SQL query and returns the results as a bytes object.

        Parameters
        ----------
        query : str
            The SQL query to execute.
        timeout_in_seconds : int
            The maximum amount of time to wait for the query to complete.

        Returns
        -------
        bytes
            The results of the query as a bytes object.
        """

        response = self.athena.start_query_execution(
            QueryString=query,
            ResultConfiguration={"OutputLocation": self.result_output_location}
        )

        execution_id = response["QueryExecutionId"]

        state = "RUNNING"
        state_change_reason = ""

        # get start time
        start_time = time.time()

        while state in ["RUNNING", "QUEUED"]:
            response = self.athena.get_query_execution(QueryExecutionId=execution_id)
            if (
                    "QueryExecution" in response
                    and "Status" in response["QueryExecution"]
                    and "State" in response["QueryExecution"]["Status"]
            ):
                state = response["QueryExecution"]["Status"]["State"]
                if state == "SUCCEEDED":
                    break

                elif "StateChangeReason" in response["QueryExecution"]['Status']:
                    state_change_reason = response["QueryExecution"]['Status']['StateChangeReason']
                    time.sleep(1)

            # check if timeout has been exceeded and raise timeout exception
            if time.time() - start_time > timeout_in_seconds:
                raise Exception(
                    "Query timeout exceeded. Query state: " + state + " -- Query state change reason: " + state_change_reason)

                # check if query failed and raise exception
        if state != 'SUCCEEDED':
            raise Exception("Query state: " + state + " -- Query state change reason: " + state_change_reason)

        response = self.s3.Bucket(self.bucket_name).Object(key=execution_id + ".csv").get()
        return response['Body'].read()
