from braket.circuits.noise_model import (
    GateCriteria,
    NoiseModel,
    ObservableCriteria,
)
from braket.circuits import Circuit, Observable, Gate
from braket.circuits.noises import (
    BitFlip,
    Depolarizing,
    TwoQubitDepolarizing,
)
from braket.devices import LocalSimulator
import numpy as np
import math


class fidelity_classifier:
    def __init__(self, n, device, noise_model):
        self.n = n
        self.device = device
        self.noise_model = noise_model

    def create_hadamard_circuit(self, gate_num=2):
        c = Circuit()
        for qubit in range(self.n):
            for _ in range(gate_num):
                c.h(qubit)
        c = self.noise_model.apply(c)
        return c

    def single_qubit_fidelity(self, had_cnt=2):
        c = self.create_hadamard_circuit(had_cnt)
        shotnum = 10000
        task = self.device.run(c, shots=shotnum)
        result = task.result()
        measurement = result.measurement_counts
        measurement = {int(state[::-1], 2): cnt for state, cnt in measurement.items()}
        return [
            (
                sum(
                    cnt
                    for state, cnt in measurement.items()
                    if not (state & (2**qubit))
                )
                / shotnum
            )
            ** 0.5
            for qubit in range(self.n)
        ]

    def create_round_robin(self):
        # Round Robin Creation
        rownum = self.n - 1 + (self.n & 1)
        colnum = (self.n + 1) // 2

        table = [[] for _ in range(rownum)]

        cur = 0

        for row in range(rownum):
            for col in range(colnum):
                table[row].append([cur])
                cur += 1
                cur %= self.n + 1 - (self.n & 1)

        for row in range(rownum):
            place_row = (row - 1) % rownum
            for col in range(colnum - 1, -1, -1):
                place_col = colnum - 1 - col
                table[place_row][place_col].append(table[row][col][0])
            if not self.n & 1:
                table[place_row][place_col][1] = self.n - 1

        for row in range(rownum):
            cur = []
            for col in range(colnum):
                cur.append(table[row][col][::-1])
            table.append(cur)

        return table

    def two_qubit_fidelity(self):
        two_q_fidelity = np.zeros((self.n, self.n))
        table = self.create_round_robin()
        for round in table:
            c = Circuit()
            for a, b in round:
                if a == b:
                    c.i(a)
                    continue
                c.h(a)
                c.cnot(a, b)
            c = self.noise_model.apply(c)

            shotnum = 10000
            task = self.device.run(c, shots=shotnum)
            result = task.result()
            measurement = result.measurement_counts
            measurement = {
                int(state[::-1], 2): cnt for state, cnt in measurement.items()
            }

            for a, b in round:
                if a == b:
                    continue
                cur_cnt = 0
                for state, cnt in measurement.items():
                    if state & (1 << a) and state & (1 << b):
                        cur_cnt += cnt
                    if (not state & (1 << a)) and (not state & (1 << b)):
                        cur_cnt += cnt
                two_q_fidelity[a][b] = cur_cnt / shotnum

        print(two_q_fidelity, sep="\n")
