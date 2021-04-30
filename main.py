import cirq
from cirq import Simulator, measure, ZZPowGate, ZZ, GridQubit
from cirq.ops import CZ, H, ISWAP, ISwapPowGate, rx, ry, rz, Z, X, CNOT
import random
import numpy as np
import matplotlib.pyplot as plt

def setup_qubits():
    qubits=[]
    for i in range(8):
        for j in range(3):
            qubits.append(GridQubit(i, j))
    return qubits

