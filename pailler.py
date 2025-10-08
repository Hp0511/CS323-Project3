"""
File: pailler.py
Description: This file contains method for averaging with Pailler protection of averaging n different integers.
"""

from phe import paillier
import time
import numpy as np

def paillier_avg(arr):
    public_key, private_key = paillier.generate_paillier_keypair()
    encrypted_vals = [public_key.encrypt(v) for v in arr]
    encrypted_sum = sum(encrypted_vals)
    total_sum = private_key.decrypt(encrypted_sum)
    return total_sum/len(arr)

