import numpy as np
from simulator import H, QuantumState, apply_single_gate

# Test 1: Precision Drift
print("--- Precision Test ---")
qs = QuantumState(1)
for _ in range(1000):
    apply_single_gate(qs, H, target_qubit=0)

prob_sum = np.sum(qs.probabilities())
print(f"Probability sum after 1000 H gates: {prob_sum:.16f}")
print(f"Is normalized?: {qs.check_normalized()}")
print(f"Drift error: {abs(1.0 - prob_sum):.16e}\n")

# Test 2: Memory Scaling Limit
print("--- Scaling Limit Test ---")
for n in range(14, 25):
    try:
        bytes_needed = (2**n) * 16
        mb_needed = bytes_needed / (1024**2)
        print(f"Qubits: {n:>2} | Vector Size: {2**n:>10} | RAM: {mb_needed:>8.2f} MB", end="")
        qs = QuantumState(n)
        print(" -> Allocated successfully")
    except MemoryError:
        print(" -> FAILED (Memory Error / Out of RAM)")
        break