import time
import matplotlib.pyplot as plt
import numpy as np
from simulator import H, QuantumState, apply_cnot, apply_single_gate


def measure_kpis(num_qubits):
    # State vector size (KPI 5) — theoretical size 2^n
    state_vector_size = 2**num_qubits

    # Memory usage (KPI 2) — actual bytes occupied in memory
    qs = QuantumState(num_qubits)
    memory_bytes = qs.state.nbytes

    # Gate execution time (KPI 6) — single H gate execution time
    start = time.perf_counter()
    apply_single_gate(qs, H, target_qubit=0)
    gate_time = time.perf_counter() - start

    # Execution time (KPI 1) — time for full circuit (H on every qubit)
    qs2 = QuantumState(num_qubits)
    start = time.perf_counter()
    for q in range(num_qubits):
        apply_single_gate(qs2, H, target_qubit=q)
    total_time = time.perf_counter() - start

    # Probability correctness (KPI 4)
    probs = qs2.probabilities()
    correct = np.isclose(np.sum(probs), 1.0)

    return {
        "num_qubits": num_qubits,
        "state_vector_size": state_vector_size,
        "memory_bytes": memory_bytes,
        "gate_time_sec": gate_time,
        "total_time_sec": total_time,
        "probabilities_sum_to_1": correct,
    }


if __name__ == "__main__":
    print(
        f"{'qubits':>7} {'vector size':>12} {'memory (KB)':>12} {'gate time (ms)':>15} {'total time (ms)':>16} {'correct':>8}"
    )
    results = []
    for n in range(1, 13):  # try 1 to 12 qubits
        r = measure_kpis(n)
        results.append(r)
        print(
            f"{r['num_qubits']:>7} {r['state_vector_size']:>12} "
            f"{r['memory_bytes']/1024:>12.2f} {r['gate_time_sec']*1000:>15.4f} "
            f"{r['total_time_sec']*1000:>16.4f} {str(r['probabilities_sum_to_1']):>8}"
        )

    # --- Generate Plots for Technical Report ---
    qubits = [r["num_qubits"] for r in results]
    vector_sizes = [r["state_vector_size"] for r in results]
    total_times = [r["total_time_sec"] * 1000 for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: State Vector Size vs Qubits
    ax1.plot(qubits, vector_sizes, "o-", color="purple")
    ax1.set_title("State Vector Size vs Qubits")
    ax1.set_xlabel("Number of Qubits (n)")
    ax1.set_ylabel("State Vector Size (2^n)")
    ax1.grid(True)

    # Plot 2: Total Execution Time vs Qubits
    ax2.plot(qubits, total_times, "o-", color="green")
    ax2.set_title("Total Execution Time vs Qubits")
    ax2.set_xlabel("Number of Qubits (n)")
    ax2.set_ylabel("Execution Time (ms)")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("kpi_benchmark_plots.png")
    print("\nPlots saved as 'kpi_benchmark_plots.png'!")
    plt.show()