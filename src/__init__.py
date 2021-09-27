import logging
import time

import numpy as np

logger = '../data/logs.log'
logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d :: %(message)s',
                    level=logging.INFO, filename=logger, filemode='a')


def time_counter(fun):
    def counter(*args, **kwargs):
        start_time = time.time()
        a = fun(*args, **kwargs)
        end_time = time.time()
        perf_time = end_time - start_time
        if perf_time > 3600:
            perf_time = np.round(perf_time / 3600, 2)
            measure = 'H'
        elif perf_time > 60:
            perf_time = np.round(perf_time / 60, 2)
            measure = 'min.'
        else:
            perf_time = np.round(perf_time, 2)
            measure = 'sek.'
        logging.info(f'Performance time: {perf_time} {measure}')
        return a

    return counter
