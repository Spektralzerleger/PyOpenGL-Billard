"""
Last modified: 28.06.2020
Time help functions...
"""

import time

my_time_initialized = False
start_time = time.time()


def diff_seconds():
    """Function that calculates the time difference between two calls of this function.

    Returns:
        float: Time difference in seconds.
    """
    global my_time_initialized
    global start_time

    if my_time_initialized == False:
        my_time_initialized = True
        start_time = time.time()

    diff = time.time() - start_time
    start_time = time.time()

    return diff
