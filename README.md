# Quantum Circuit Simulator (Python & NumPy)

A state-vector quantum circuit simulator built from scratch using Python and NumPy. This project implements fundamental single-qubit gates, multi-qubit entanglement via CNOT, measurement sampling, performance benchmarking, and hardware scalability analysis.

---

## 1. Project Structure

* `simulator.py` — Core quantum simulator class (`QuantumState`), single/multi-qubit gate logic (`apply_single_gate`, `apply_cnot`), and Bell state circuit.
* `benchmark.py` — Benchmark suite measuring state vector memory scaling, gate execution times, and probability correctness across $1$ to $12$ qubits.
* `failure_test.py` — Stress tests for floating-point precision drift and memory allocation limits.
* `kpi_benchmark_plots.png` — Plot graphs displaying exponential memory and execution time scaling.

---

## 2. Core Simulator Verification & Bell State Results

### Single-Qubit & Bell State Circuit Execution
The simulator was verified by creating a 2-qubit Bell state $\vert{}\Phi^+\rangle = \frac{1}{\sqrt{2}}(\vert{}00\rangle + \vert{}11\rangle)$ using a Hadamard gate on qubit 0 followed by a CNOT gate targeted at qubit 1.

* **State Vector Output:** `[0.70710678+0.j, 0.+0.j, 0.+0.j, 0.70710678+0.j]`
* **Calculated Probabilities:** `[0.5, 0.0, 0.0, 0.5]` ($50\%$ chance for $\vert{}00\rangle$, $50\%$ chance for $\vert{}11\rangle$)
* **Normalization Check:** `True` ($\sum P(x) = 1.0$)

### 1000 Measurement Shots Sampling
Running 1000 measurement shots on the Bell state confirmed expected quantum statistics with zero illegal state outcomes (`01` or `10`):

```text
Counter({'00': 504, '11': 496})