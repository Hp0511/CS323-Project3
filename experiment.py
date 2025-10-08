"""
File: experiments.py
Description: This file contains different helper functions for the main program.
"""
import random, time

def gen_arr(n, lo=0, hi=10_000, seed=None):
    rnd = random.Random(seed)
    return [rnd.randrange(lo, hi) for _ in range(n)]

def time_run(fn, data):
    t0 = time.perf_counter()
    _ = fn(data)
    return time.perf_counter() - t0
