import dwave_micro_client_dimod as system

from dwave_circuit_fault_diagnosis_demo import *  # TODO

if __name__ == '__main__':
    bqm, labels = three_bit_multiplier()

    # get input from user
    fixed_variables = {}

    got = False
    while not got:
        try:
            A = int(input("Input multiplier A (<=7):"))
            fixed_variables['a2'], fixed_variables['a1'], fixed_variables['a0'] = "{:3b}".format(A)
            got = True
        except ValueError:
            pass

    got = False
    while not got:
        try:
            B = int(input("Input multiplicand B (<=7):"))
            fixed_variables['b2'], fixed_variables['b1'], fixed_variables['b0'] = "{:3b}".format(B)
            got = True
        except ValueError:
            pass

    got = False
    while not got:
        try:
            P = int(input("Input product P (<=63):"))
            fixed_variables['p5'], fixed_variables['p4'], fixed_variables['p3'], fixed_variables['p2'], fixed_variables['p1'], fixed_variables['p0'] = "{:6b}".format(P)
            got = True
        except ValueError:
            pass

    fixed_variables = {var: 1 if x == '1' else -1 for (var, x) in fixed_variables.items()}

    # fix variables
    for var, value in fixed_variables.items():
        bqm.fix_variable(var, value)
    # 'aux1' becomes disconnected, so needs to be fixed
    bqm.fix_variable('aux1', 1)  # don't care value

    # find embedding and put on system
    sampler = system.EmbeddingComposite(system.DWaveSampler(permissive_ssl=True))
    response = sampler.sample_ising(bqm.linear, bqm.quadratic, num_reads=1000)

    print()

    # output results
    best_sample = next(response.samples())
    best_sample.update(fixed_variables)

    for gate_type, gates in labels.items():
        _, configurations = GATES[gate_type]
        for gate_name, gate in gates.items():
            res = tuple(best_sample[var] for var in gate)
            if res in configurations:
                print('{} - valid {}'.format(gate_name, res))
            else:
                print('{} - fault {}'.format(gate_name, res))