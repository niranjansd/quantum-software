# pylint: disable=wrong-or-nonexistent-copyright-notice
import numpy as np
import cirq


def bitstring(bits):
    return ''.join('1' if e else '_' for e in bits)


class CHSHBell(object):

    def __init__(self, repetitions=1):
        super().__init__()
        self.repetitions = repetitions

    def make_bell_test_circuit(self):
        alice = cirq.GridQubit(0, 0)
        bob = cirq.GridQubit(1, 0)
        alice_referee = cirq.GridQubit(0, 1)
        bob_referee = cirq.GridQubit(1, 1)
        circuit = cirq.Circuit()

        # Prepare shared entangled state.
        circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])

        # Referees flip coins.
        circuit.append([cirq.H(alice_referee), cirq.H(bob_referee)])

        # Players do a sqrt(X) based on their referee's coin.
        circuit.append(
            [cirq.X(alice) ** -0.25,
             cirq.CNOT(alice_referee, alice) ** 0.5,
             cirq.CNOT(bob_referee, bob) ** 0.5]
        )

        # Then results are recorded.
        circuit.append(
            [
                cirq.measure(alice, key='a'),
                cirq.measure(bob, key='b'),
                cirq.measure(alice_referee, key='x'),
                cirq.measure(bob_referee, key='y'),
            ]
        )
        return circuit

    def run_bell_test(self):
        self.circuit = self.make_bell_test_circuit()
        print('Circuit:')
        print(self.circuit)

        repetitions = 75
        print(f'Simulating {repetitions} repetitions...')
        result = cirq.Simulator().run(program=self.circuit, repetitions=repetitions)

        # Collect results.
        a = np.array(result.measurements['a'][:, 0])
        b = np.array(result.measurements['b'][:, 0])
        x = np.array(result.measurements['x'][:, 0])
        y = np.array(result.measurements['y'][:, 0])
        outcomes = a ^ b == x & y
        win_percent = len([e for e in outcomes if e]) * 100 / repetitions

        # Print data.
        print()
        print('Results')
        print('a:', bitstring(a))
        print('b:', bitstring(b))
        print('x:', bitstring(x))
        print('y:', bitstring(y))
        print('(a XOR b) == (x AND y):\n  ', bitstring(outcomes))
        print(f'Win rate: {win_percent}%')


def main():
    belltest = CHSHBell()
    belltest.run_bell_test()
    # # Create circuit.
    # circuit = make_bell_test_circuit()
    # print('Circuit:')
    # print(circuit)

    # # Run simulations.
    # print()
    # repetitions = 75
    # print(f'Simulating {repetitions} repetitions...')
    # result = cirq.Simulator().run(program=circuit, repetitions=repetitions)

    # # Collect results.
    # a = np.array(result.measurements['a'][:, 0])
    # b = np.array(result.measurements['b'][:, 0])
    # x = np.array(result.measurements['x'][:, 0])
    # y = np.array(result.measurements['y'][:, 0])
    # outcomes = a ^ b == x & y
    # win_percent = len([e for e in outcomes if e]) * 100 / repetitions

    # # Print data.
    # print()
    # print('Results')
    # print('a:', bitstring(a))
    # print('b:', bitstring(b))
    # print('x:', bitstring(x))
    # print('y:', bitstring(y))
    # print('(a XOR b) == (x AND y):\n  ', bitstring(outcomes))
    # print(f'Win rate: {win_percent}%')






if __name__ == '__main__':
    main()
