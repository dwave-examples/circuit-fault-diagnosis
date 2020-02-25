import itertools

import networkx as nx
import penaltymodel.core as pm
import dimod

GATES = {}

GATES['AND'] = (('in1', 'in2', 'out'),
                {(-1, -1, -1): 0.,
                 (-1, +1, -1): 0.,
                 (+1, -1, -1): 0.,
                 (+1, +1, +1): 0., })

GATES['OR'] = (('in1', 'in2', 'out'),
               {(-1, -1, -1): 0.,
                (-1, +1, +1): 0.,
                (+1, -1, +1): 0.,
                (+1, +1, +1): 0., })

GATES['XOR'] = (('in1', 'in2', 'out'),
                {(-1, -1, -1): 0.,
                 (-1, +1, +1): 0.,
                 (+1, -1, +1): 0.,
                 (+1, +1, -1): 0., })

GATES['HALF_ADD'] = (('augend', 'addend', 'sum', 'carry_out'),
                     {(-1, -1, -1, -1): 0.,
                      (-1, +1, +1, -1): 0.,
                      (+1, -1, +1, -1): 0.,
                      (+1, +1, -1, +1): 0.})

GATES['FULL_ADD'] = (('augend', 'addend', 'carry_in', 'sum', 'carry_out'),
                     {(-1, -1, -1, -1, -1): 0.,
                      (-1, -1, +1, +1, -1): 0.,
                      (-1, +1, -1, +1, -1): 0.,
                      (-1, +1, +1, -1, +1): 0.,
                      (+1, -1, -1, +1, -1): 0.,
                      (+1, -1, +1, -1, +1): 0.,
                      (+1, +1, -1, -1, +1): 0.,
                      (+1, +1, +1, +1, +1): 0.})


def fault_gate(gate, explicit_gap):
    nV = len(next(iter(gate)))  # Assume all the same length
    fc = {}
    for config in itertools.product((-1, 1), repeat=nV):
        if config in gate:
            fc[config] = 0
        else:
            fc[config] = explicit_gap
    return fc


FAULT_GAP = .5


def gate_model(gate_type, fault=True):
    labels, configurations = GATES[gate_type]
    if fault:
        configurations = fault_gate(configurations, FAULT_GAP)
    num_variables = len(next(iter(configurations)))
    for size in range(num_variables, num_variables+4):  # reasonable margin
        G = nx.complete_graph(size)
        nx.relabel_nodes(G, dict(enumerate(labels)), copy=False)
        spec = pm.Specification(G, labels, configurations, dimod.SPIN)
        try:
            pmodel = pm.get_penalty_model(spec)
            if pmodel is not None:
                return pmodel
        except pm.ImpossiblePenaltyModel:
            pass

    raise ValueError("unable to get the penalty model from factories")
