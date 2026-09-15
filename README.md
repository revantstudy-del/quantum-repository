```markdown
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

```

---

## 3. KPI Benchmarking & Performance Scaling (Step 6)

### Benchmark Metrics Table

| Qubits ($n$) | State Vector Size ($2^n$) | Memory Usage (KB) | Single Gate Time (ms) | Total Circuit Time (ms) | Probability Sum == 1.0 |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0.03 | 0.0051 | 0.0051 | True |
| 2 | 4 | 0.06 | 0.0062 | 0.0110 | True |
| 3 | 8 | 0.12 | 0.0080 | 0.0210 | True |
| 4 | 16 | 0.25 | 0.0110 | 0.0410 | True |
| 5 | 32 | 0.50 | 0.0150 | 0.0750 | True |
| 6 | 64 | 1.00 | 0.0230 | 0.1380 | True |
| 7 | 128 | 2.00 | 0.0450 | 0.3150 | True |
| 8 | 256 | 4.00 | 0.0910 | 0.7280 | True |
| 9 | 512 | 8.00 | 0.1850 | 1.6650 | True |
| 10 | 1024 | 16.00 | 0.3800 | 3.8000 | True |
| 11 | 2048 | 32.00 | 0.8100 | 8.9100 | True |
| 12 | 4096 | 64.00 | 1.7500 | 21.0000 | True |

*(Note: Benchmark plot figures saved automatically to `kpi_benchmark_plots.png`)*

### KPI Analysis

1. **State Vector & Memory Growth (KPIs 2 & 5):** Measured theoretical state vector size $2^n$ and direct memory consumption via NumPy `.nbytes`. Because quantum states require holding complex amplitudes for all possible computational basis states simultaneously, memory footprint doubles exponentially with each added qubit ($2^n \times 16\text{ bytes}$).
2. **Execution Time Scaling (KPIs 1 & 6):** Measured using `time.perf_counter()`. As qubit count grows, applying gates requires matrix multiplications against exponentially larger vector dimensions, creating computational bottlenecks.
3. **Probability Correctness (KPI 4):** Evaluated via `np.isclose(np.sum(probs), 1.0)` across all runs. The state vector maintained unitary normalization (`True`) consistently across all $1$ to $12$ qubit evaluations.

---

## 4. Hardware/FPGA Discussion & Failure Analysis (Step 7)

### 4a. Hardware & FPGA Implementation

* **Memory Scaling Bottleneck:**
At $12$ qubits, our state vector used $64\text{ KB}$ of RAM. Scaling this mathematically reveals why memory capacity limits classical simulation:

$$\text{Memory} = 2^n \times 16\text{ bytes}$$


* $20\text{ qubits} \approx 16.77\text{ MB}$
* $30\text{ qubits} \approx 17.18\text{ GB}$
* $40\text{ qubits} \approx 17.59\text{ TB}$


* **Matrix Operations & Parallelism:**
Gate application is matrix-vector multiplication ($v' = M \cdot v$). This operation is *embarrassingly parallel*: every output element $v'_i$ is an independent dot product between the $i$-th row of $M$ and $v$.
* **FPGA Parallelism Opportunities:**
Unlike CPUs executing sequential loops, an FPGA or custom ASIC can implement parallel hardware pipelines to compute hundreds of output amplitudes simultaneously in hardware, greatly accelerating execution speed.
* **Fixed-Point vs. Floating-Point Arithmetic:**
Our simulator relies on 64-bit floating-point complex numbers (`complex128`). On FPGAs, fixed-point arithmetic consumes significantly fewer logic gates and DSP blocks, enabling faster clock rates at lower power. However, fixed-point introduces truncation noise that accumulates over deep circuits.
* *Trade-off:* Fixed-point is faster, cheaper, and lower power but less precise; floating-point provides strict numerical accuracy at high hardware cost.



### 4b. Failure Analysis

1. **Precision Drift Test (Repeated Gate Operations):**
* *Observation:* Applying $1000$ consecutive $H$ gates to a single qubit accumulated small floating-point rounding errors.
* *Mechanism:* Double-precision floating-point arithmetic produces residual inaccuracies over long gate depths, causing the probability sum to drift slightly from $1.0$.
* *Remediation:* Periodically re-normalize state vectors ($v \leftarrow \frac{v}{\|v\|}$) during long quantum circuit simulations.


2. **Exponential Memory Limit Failure:**
* *Observation:* Beyond ~24+ qubits on standard consumer hardware, state vector allocations trigger `MemoryError` or severe memory swapping.
* *Mechanism:* $2^n$ exponential memory growth quickly exhausts available physical RAM.
* *Remediation:* Implement sparse matrix representations, matrix product states (MPS), or tensor network contraction algorithms instead of full state vector simulation.