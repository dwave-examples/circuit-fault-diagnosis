# Copyright 2018 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import dwave_micro_client_dimod as system
from dwave_circuit_fault_diagnosis_demo import *  # TODO

import pandas as pd
import pickle

original, labels = three_bit_multiplier()

DF = {}

sampler = system.EmbeddingComposite(system.DWaveSampler(permissive_ssl=True))

for i, config in enumerate(itertools.product((-1, 1), repeat=12)):
    bqm = original.copy()
    fixed_variables = dict(zip(('p5', 'p4', 'p3', 'p2', 'p1', 'p0', 'b2', 'b1', 'b0', 'a2', 'a1', 'a0'), config))

    # fix variables
    for var, value in fixed_variables.items():
        bqm.fix_variable(var, value)
    # 'aux1' becomes disconnected, so needs to be fixed
    bqm.fix_variable('aux1', 1)  # don't care value

    # find embedding and put on system
    while True:
        try:
            response = sampler.sample_ising(bqm.linear, bqm.quadratic, num_reads=1000)
        except ValueError:
            pass
        else:
            break

    # output results
    best_sample = next(response.samples())
    best_sample.update(fixed_variables)

    for gate_type, gates in labels.items():
        _, configurations = GATES[gate_type]
        for gate_name, gate in gates.items():
            res = tuple(best_sample[var] for var in gate)
            fixed_variables[gate_name] = res in configurations

    print(i, fixed_variables)
    DF[i] = fixed_variables

DF = pd.DataFrame(DF)
with open('DF.pickle', 'wb') as f:
    pickle.dump(DF, f)
