import boto3
import time


def run_crawler(crawler: str, timeout_in_seconds: int) -> None:
    """
    Runs a Glue crawler and waits for it to finish.

    Parameters
    ----------
    crawler : str
        The name of the crawler to run.
    timeout_in_seconds : int
        The maximum amount of time to wait for the crawler to complete.

    Returns
    -------
    None
    """

    client = boto3.client("glue")

    # get start time
    start_time = time.time()

    def wait_until_ready() -> None:
        state_previous = None
        while True:
            response_get = client.get_crawler(Name=crawler)
            state = response_get["Crawler"]["State"]
            if state != state_previous:
                state_previous = state
            if state == "READY":  # Other known states: RUNNING, STOPPING
                return

            # check if timeout has been exceeded and raise timeout exception
            if time.time() - start_time > timeout_in_seconds:
                raise TimeoutError(
                    f"Failed to crawl {crawler}. The allocated time of {timeout_in_seconds} seconds has elapsed.")
            time.sleep(1)

    response_start = client.start_crawler(Name=crawler)
    assert response_start["ResponseMetadata"]["HTTPStatusCode"] == 200
    wait_until_ready()