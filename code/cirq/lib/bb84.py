# BB84
## Imports
import numpy as np
import cirq


## Utility functions
def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)


class BB84(object):

    def __init__(self, repetitions=1, random_seed=200):
        super().__init__()
        np.random.seed(random_seed)  # Seed random generator for consistent results
        self.repetitions = repetitions
        self.circuits = {}

    def setup_demo(self, num_qubits):
        self.alice_basis = [np.random.randint(0, 2) for _ in range(num_qubits)]
        self.alice_state = [np.random.randint(0, 2) for _ in range(num_qubits)]
        self.bob_basis = [np.random.randint(0, 2) for _ in range(num_qubits)]
        self.eve_basis = [np.random.randint(0, 2) for _ in range(num_qubits)]
        self.expected_key = bitstring(
            [self.alice_state[i] for i in range(num_qubits) if self.alice_basis[i] == self.bob_basis[i]]
        )

    def make_bb84_circuit(self, num_qubits, sender_basis, receiver_basis, sender_state, name="1"):
        self.qubits = cirq.LineQubit.range(num_qubits)
        self.circuits[name] = cirq.Circuit()

        # Sender prepares her qubits
        sender_flips = []
        sender_rotations = []
        for index, _ in enumerate(sender_basis):
            if sender_state[index] == 1:
                sender_flips.append(cirq.X(self.qubits[index]))
            if sender_basis[index] == 1:
                sender_rotations.append(cirq.H(self.qubits[index]))
        sender_moment1 = cirq.Moment(sender_flips)
        sender_moment2 = cirq.Moment(sender_rotations)
        self.circuits[name].append(sender_moment1)
        self.circuits[name].append(sender_moment2)

        # Receiver measures the received qubits
        recv_basis_choice = []
        for index, rbasis in enumerate(receiver_basis):
            if rbasis == 1:
                recv_basis_choice.append(cirq.H(self.qubits[index]))
        recv_moment = cirq.Moment(recv_basis_choice)
        self.circuits[name].append(recv_moment)
        self.circuits[name].append(cirq.Moment(cirq.measure_each(*self.qubits)))

    def simulate_base_protocol(self, num_qubits=8, print_legend=None):
        self.setup_demo(num_qubits)

        # First Alice creates and sends message to Bob.
        self.make_bb84_circuit(num_qubits, self.alice_basis, self.bob_basis,
                               self.alice_state, name="base")

        # Bob measures the received qubits.
        result = cirq.Simulator().run(program=self.circuits["base"], repetitions=self.repetitions)
        result_bitstring = bitstring([int(result.measurements[str(q)]) for q in self.qubits])

        # Bob gets Alice's public key and only keeps bits where bases match.
        obtained_key = ''.join(
            [result_bitstring[i] for i in range(num_qubits) if self.alice_basis[i] == self.bob_basis[i]]
        )

        # Print results.
        print_legend = self.print_legend if print_legend is None else print_legend
        if print_legend:
            print("######### Printing legend ##########")
            self.print_legend()
        print("########## Printing circuit ##########")
        print(self.circuits["base"])
        print("########## Printing results ##########")
        self.print_results(self.alice_basis, self.bob_basis, self.alice_state,
                           self.expected_key, obtained_key)
        print("The next message can be sent on classical channel encrypted with this shared secret key.")

    def simulate_eavesdropped_protocol(self, num_qubits=8, print_legend=None):
        self.setup_demo(num_qubits)

        # Eve intercepts Alice's message.
        # So we have two messages being sent, Alice to Eve and Eve to Bob.
        # First Alice creates and sends message to Eve.
        self.make_bb84_circuit(num_qubits, self.alice_basis, self.eve_basis,
                               self.alice_state, name="alice_eve")

        # Eve measures and then tries to recreate Alice's message.
        result = cirq.Simulator().run(program=self.circuits["alice_eve"],
                                      repetitions=self.repetitions)
        eve_state = [int(result.measurements[str(q)]) for q in self.qubits]

        # Eve sends message to Bob.
        self.make_bb84_circuit(num_qubits, self.eve_basis, self.bob_basis, eve_state, name="eve_bob")

        # Bob measures the received qubits.
        result = cirq.Simulator().run(program=self.circuits["eve_bob"], repetitions=self.repetitions)
        result_bitstring = bitstring([int(result.measurements[str(q)]) for q in self.qubits])

        # Eve gets Alice's public key and only keeps bits where bases match.
        intercepted_key = ''.join(
            [result_bitstring[i] for i in range(num_qubits) if self.alice_basis[i] == self.eve_basis[i]]
        )
        # Bob gets Alice's public key and only keeps bits where bases match.
        obtained_key = ''.join(
            [result_bitstring[i] for i in range(num_qubits) if self.alice_basis[i] == self.bob_basis[i]]
        )

        # Print results.
        circuit = self.circuits["alice_eve"] + self.circuits["eve_bob"]
        print_legend = self.print_legend if print_legend is None else print_legend
        if print_legend:
            print("######### Printing legend ##########")
            self.print_legend()
        print("########## Printing circuit ##########")
        print(circuit)
        print("########## Printing results ##########")
        self.print_eavesdropped_results(
            self.alice_basis, self.bob_basis, self.eve_basis, self.alice_state, eve_state,
             self.expected_key, obtained_key)
        print("""Alice sends the next message on classical channel encrypted with her key.
    If Eve is still listening she can decrypt the message.
    But since Bob cannot decrypt the message they will know something went wrong.
    So the first message can be a known dummy message,
    for example, Alice can resend her already public basis
    so that Eve is detected before any secret information is leaked.""")

    def print_legend(self):
        print("Bases : C = Computational Basis (0,1); H = Hadamard Basis (+, -)")
        print("Gates : X = Pauli X; H = Hadamard; M = Measurement")

    def print_results(self, alice_basis, bob_basis, alice_state, expected_key, obtained_key):
        num_qubits = len(alice_basis)
        basis_match = ''.join(
            ['X' if alice_basis[i] == bob_basis[i] else '_' for i in range(num_qubits)]
        )
        alice_basis_str = "".join(['C' if alice_basis[i] == 0 else "H" for i in range(num_qubits)])
        bob_basis_str = "".join(['C' if bob_basis[i] == 0 else "H" for i in range(num_qubits)])

        print(f'Only Alice knows Alice\'s message:\t{bitstring(alice_state)}')
        print('After Bob\'s measurement, the bases are made public: ')
        print(f'Alice\'s basis:\t{alice_basis_str}')
        print(f'Bob\'s basis:\t{bob_basis_str}')
        print(f'Bases match::\t{basis_match}')

        print(f'Key according to Alice:\t{expected_key}')
        print(f'Key according to Bob:\t{obtained_key}')

    def print_eavesdropped_results(self, alice_basis, bob_basis, eve_basis, alice_state,
                                   eve_state, expected_key, obtained_key):
        num_qubits = len(alice_basis)
        eve_basis_match = ''.join(
            ['X' if alice_basis[i] == eve_basis[i] else '_' for i in range(num_qubits)]
        )
        bob_basis_match = ''.join(
            ['X' if alice_basis[i] == bob_basis[i] else '_' for i in range(num_qubits)]
        )
        alice_basis_str = "".join(['C' if alice_basis[i] == 0 else "H" for i in range(num_qubits)])
        eve_basis_str = "".join(['C' if eve_basis[i] == 0 else "H" for i in range(num_qubits)])
        bob_basis_str = "".join(['C' if bob_basis[i] == 0 else "H" for i in range(num_qubits)])

        print(f'Only Alice knows Alice\'s message:\t{bitstring(alice_state)}')
        print(f'Eve\'s best guess for Alice\'s state is:\t{bitstring(eve_state)}')

        print('After Bob\'s measurement, the bases are made public: ')
        print(f'Alice\'s basis:\t{alice_basis_str}')
        print(f'Eve\'s basis:\t{eve_basis_str}')
        print(f'Bob\'s basis:\t{bob_basis_str}')

        print(f'Eve\'s bases match::\t{eve_basis_match}')
        print(f'Bob\'s bases match::\t{bob_basis_match}')

        print(f'Key according to Alice:\t{expected_key}')
        print(f'Key according to Eve:\t{expected_key}')
        print(f'Key according to Bob:\t{obtained_key}')
