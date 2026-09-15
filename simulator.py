import numpy as np


class QuantumState:

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        size = 2**num_qubits
        self.state = np.zeros(size, dtype=complex)
        self.state[0] = 1.0

    def probabilities(self):
        return np.abs(self.state) ** 2

    def check_normalized(self):
        total = np.sum(self.probabilities())
        return np.isclose(total, 1.0)

    def measure(self):
        probs = self.probabilities()
        outcome = np.random.choice(len(self.state), p=probs)
        return format(outcome, f"0{self.num_qubits}b")


# --- Single-qubit gates (2x2 matrices) ---
I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
Z = np.array([[1, 0], [0, -1]])


def apply_single_gate(state_obj, gate, target_qubit):
    ops = [I] * state_obj.num_qubits
    ops[target_qubit] = gate
    full_matrix = ops[0]
    for op in ops[1:]:
        full_matrix = np.kron(full_matrix, op)
    state_obj.state = full_matrix @ state_obj.state


def apply_cnot(state_obj, control_qubit, target_qubit):
    n = state_obj.num_qubits
    size = 2**n
    new_state = np.zeros(size, dtype=complex)
    for i in range(size):
        bits = list(format(i, f"0{n}b"))
        if bits[control_qubit] == "1":
            bits[target_qubit] = (
                "0" if bits[target_qubit] == "1" else "1"
            )
        j = int("".join(bits), 2)
        new_state[j] = state_obj.state[i]
    state_obj.state = new_state


def apply_swap(state_obj, qubit1, qubit2):
    n = state_obj.num_qubits
    size = 2**n
    new_state = np.zeros(size, dtype=complex)
    for i in range(size):
        bits = list(format(i, f"0{n}b"))
        bits[qubit1], bits[qubit2] = bits[qubit2], bits[qubit1]
        j = int("".join(bits), 2)
        new_state[j] = state_obj.state[i]
    state_obj.state = new_state


# --- Step 5: Build and run a full circuit ---
def bell_state_circuit():
    qs = QuantumState(2)  # start at |00>
    apply_single_gate(qs, H, target_qubit=0)
    apply_cnot(qs, control_qubit=0, target_qubit=1)
    return qs


if __name__ == "__main__":
    qs = bell_state_circuit()
    print("State vector:", qs.state)
    print("Probabilities:", qs.probabilities())
    print("Normalized OK?", qs.check_normalized())
    print("One measurement:", qs.measure())

    # --- Run 1000 measurements (shots) ---
    from collections import Counter

    shots = 1000
    results = [qs.measure() for _ in range(shots)]
    counts = Counter(results)

    print("\n--- 1000 Measurement Results ---")
    print(counts)