# Technical Report: Hybrid Quantum Circuit Simulator

## 1. Implementation Approach & Gate Explanation

### Quantum State Representation
A quantum system with $n$ qubits resides in a $2^n$-dimensional Hilbert space. The state vector is represented using NumPy array amplitudes ($c_i \in \mathbb{C}$) initialized with data type `complex128`.

The quantum state $|\psi\rangle$ is given by:
$$|\psi\rangle = \sum_{i=0}^{2^n-1} c_i |i\rangle \quad \text{where} \quad \sum_{i=0}^{2^n-1} |c_i|^2 = 1$$

* **Superposition:** Created by applying gates like Hadamard ($H$), distributing probability amplitudes across multiple basis states simultaneously.
* **Probabilities:** Computed via Born's rule $P(i) = |c_i|^2$. Sampling measurements over $N$ shots projects the quantum state into classical binary outcomes.

### Unitary Gate Operations
* **Single-Qubit Gates:** Constructed across $n$ qubits using Kronecker tensor products ($\otimes$) with $2 \times 2$ matrices and Identity ($I$):
  $$U_{\text{full}} = I \otimes \dots \otimes U_{\text{gate}} \otimes \dots \otimes I$$
  * **Pauli-X ($X$):** Bit-flip gate ($\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$).
  * **Hadamard ($H$):** Superposition gate ($\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$).
  * **Pauli-Z ($Z$):** Phase-flip gate ($\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$).
* **Two-Qubit Gates ($\text{CNOT}$):** Implemented via computational basis bit manipulation, toggling the target qubit amplitude index if the control bit is set to $1$.

---

## 2. Circuit Execution & KPI Discussion

### Bell State Circuit Workflow
A 2-qubit entangled Bell state $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$ was executed:
1. Initialize $|\psi_0\rangle = |00\rangle$.
2. Apply $H$ to qubit 0 $\implies \frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)$.
3. Apply $\text{CNOT}$ (control=0, target=1) $\implies \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$.

**1000 Shots Measurement Output:**
`Counter({'00': 504, '11': 496})` — Confirms expected $50/50$ probabilistic distribution without illegal $|01\rangle$ or $|10\rangle$ outcomes.

### KPI Analysis
* **State Vector Size ($2^n$):** Grows exponentially. At $12$ qubits, size is $4,096$ complex numbers.
* **Memory Usage:** Evaluated via `.nbytes`. At $n=12$, memory usage is $64\text{ KB}$. Beyond $n \ge 30$, physical RAM ($\sim 17.18\text{ GB}$) becomes the dominant bottleneck.
* **Execution & Gate Time:** Measured using `time.perf_counter()`. Increases exponentially due to $2^n \times 2^n$ matrix-vector multiplication overhead.
* **Probability Correctness:** Confirmed via $\sum |c_i|^2 = 1.0$ across all tested qubit counts.

---

## 3. Hardware Acceleration & FPGA Analysis

* **Parallelism Opportunities:** Updating state vectors ($v' = M \cdot v$) is embarrassingly parallel. On FPGAs or custom ASICs, hundreds of rows can be evaluated simultaneously using parallel Multiply-Accumulate (MAC) units.
* **Memory Bottleneck:** Storing full state vectors requires $2^n \times 16\text{ bytes}$. FPGAs are bound by onboard Block RAM (BRAM), limiting raw state vector simulation without external high-bandwidth memory (HBM).

---

## 4. Brownie-Point Challenges

### Challenge B — Fixed-Point Analysis
* **Floating-Point (`complex128`):** Provides extreme precision ($15+$ decimal places) but requires complex floating-point hardware units, consuming excessive DSP slices and logic on FPGAs.
* **Fixed-Point Arithmetic:** Uses integer registers with a fixed fractional split (e.g., Q2.14 format). It reduces hardware resource usage by $>60\%$ and drastically increases clock throughput.
* **Trade-off:** Fixed-point accumulates truncation/rounding noise over deep quantum circuits, leading to loss of state normalization ($\sum |c_i|^2 \neq 1.0$) unless periodic re-normalization logic is implemented.

### Challenge C — Hardware-Aware Optimizations
1. **Sparse Storage:** Many quantum states have large numbers of zero amplitudes. Storing only non-zero entries reduces memory from $O(2^n)$ to $O(k)$ where $k \ll 2^n$.
2. **Gate Fusion:** Multiple sequential gates ($U_1, U_2, U_3$) targeting the same qubit can be pre-multiplied into a single combined matrix $U_{\text{fused}} = U_3 \cdot U_2 \cdot U_1$, cutting total matrix-vector multiplications by $3\times$.

---

## 5. Failure Analysis

1. **Floating-Point Precision Drift:** Applying $1,000$ consecutive Hadamard gates accumulates small floating-point rounding errors ($1.0000000000000002$). *Mitigation:* Periodically apply $v \leftarrow \frac{v}{\|v\|}$.
2. **Exponential Memory Exhaustion:** Attempting $n \ge 25$ qubits raises `MemoryError` on consumer hardware ($> 268\text{ MB}$ to several GBs). *Mitigation:* Transition from dense state vectors to Matrix Product States (MPS) or Tensor Networks.