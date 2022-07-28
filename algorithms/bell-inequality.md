---
description: The flagship experiment of quantum physics
---

# Bell Inequality

[Bell's theorem](https://en.wikipedia.org/wiki/Bell's\_theorem) proves that quantum entanglement cannot be explained by any [local realist theory](https://en.wikipedia.org/wiki/Principle\_of\_locality#Quantum\_mechanics). Bell inequality has been tested experimentally for more than 50 years and has proven conclusively that reality is not local realist, **reality is quantum**.

### Objective

Setup an experiment showing that entangled states are nonlocal, i.e. measuring one part of the entangled state affects the other part instantaneously. In other words, demonstrate "spooky action at a distance".

### Prerequisite

* An oracle that can create 2 qubits in any arbitrary state and send 1 qubit to Alice and 1 to Bob.&#x20;
* Alice and Bob can measure their qubits in any basis.
* Alice and Bob can decide together what bases they use, but they cannot change the basis based on the other measurement. This can be enforced by making the distance between them is greater than what light can travel in the time difference between the two measurements.

### Run protocol

Alice and Bob are told what state the oracle makes. If Alice receives state x and Bob receives state y respectively and Alice's measurement returns a and Bob's returns b, then their goal is choose a basis such that&#x20;

$$
a XOR b = x AND y
$$

For every state made by the oracle, the experiment is run many times and Alice and Bob report the probability of the condition being true.

### Classical best case

For any product state the oracle makes, i.e. Alice's state is separable from Bob's state,  Alice and Bob can only win at most 75% of the time.

### Quantum best case

If the oracle makes an entangled Bell state, Alice and Bob can find a basis that wins 85% of the time.&#x20;

### Real case

In practice, entangled states decohere due to noise. Therefore 85% is never achievable in practice. However, exceeding 75% is used as a proof that the oracle is indeed making non-classical, at least partially entangled states.
