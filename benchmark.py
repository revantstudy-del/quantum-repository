import time
import numpy as np
import matplotlib.pyplot as plt
from simulator import QuantumState, H, apply_single_gate

def run_benchmarks(max_qubits=12):
    qubit_counts = list(range(1, max_qubits + 1))
    memory_kb_list = []
    gate_times_ms = []
    circuit_times_ms = []
    is_normalized_list = []

    print(f"{'Qubits':<8}{'Size (2^n)':<12}{'Memory (KB)':<14}{'Gate Time (ms)':<16}{'Circuit Time (ms)':<20}{'Normalized':<10}")
    print("-" * 80)

    for n in qubit_counts:
        qs = QuantumState(n)
        
        # Benchmark Single Gate Time
        t0 = time.perf_counter()
        apply_single_gate(qs, H, target_qubit=0)
        t1 = time.perf_counter()
        gate_time = (t1 - t0) * 1000

        # Benchmark Full Circuit (H applied across all qubits)
        qs_circuit = QuantumState(n)
        t_start = time.perf_counter()
        for q in range(n):
            apply_single_gate(qs_circuit, H, target_qubit=q)
        t_end = time.perf_counter()
        circuit_time = (t_end - t_start) * 1000

        memory_kb = qs.state.nbytes / 1024
        normalized = qs_circuit.check_normalized()

        memory_kb_list.append(memory_kb)
        gate_times_ms.append(gate_time)
        circuit_times_ms.append(circuit_time)
        is_normalized_list.append(normalized)

        print(f"{n:<8}{2**n:<12}{memory_kb:<14.2f}{gate_time:<16.4f}{circuit_time:<20.4f}{str(normalized):<10}")

    # Generate Performance Plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(qubit_counts, memory_kb_list, marker='o', color='b')
    ax1.set_title("Memory Scaling (KB)")
    ax1.set_xlabel("Number of Qubits")
    ax1.set_ylabel("Memory Usage (KB)")
    ax1.grid(True)

    ax2.plot(qubit_counts, circuit_times_ms, marker='s', color='r')
    ax2.set_title("Total Execution Time (ms)")
    ax2.set_xlabel("Number of Qubits")
    ax2.set_ylabel("Time (ms)")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("kpi_benchmark_plots.png")
    print("\nBenchmark plots successfully saved as 'kpi_benchmark_plots.png'.")

if __name__ == "__main__":
    run_benchmarks(12)