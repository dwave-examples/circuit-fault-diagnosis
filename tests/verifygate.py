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

import pandas as pd
import dimod


def verifygate(bqm, vars):
    es = dimod.ExactSolver()
    resp = es.sample_ising(bqm.linear, bqm.quadratic)
    resp = resp.as_binary()
    # Q = {(k, k): v for k, v in bqm.linear.items()}
    # Q.update(bqm.quadratic)
    # resp = es.sample_qubo(Q)

    df = pd.DataFrame([dict(data['sample'], **{'energy': data['energy']}) for data in resp.data()])

    return df.groupby(vars).energy.agg(min).reset_index().sort_values('energy')
