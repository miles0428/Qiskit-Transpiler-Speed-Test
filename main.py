import qiskit as qk 
import numpy as np
import matplotlib.pyplot as plt
import time
from qiskit_ibm_runtime.fake_provider import FakeCairoV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def callback_func(**kwargs):
    global excute_info
    pass_ = kwargs['pass_']
    time = kwargs['time']
    count = kwargs['count']
    name = pass_.__class__.__name__
    excute_info.append([name, time, count])
    
for num_qubits in range(10,15):
    excute_info = []
    state = np.random.rand(2**num_qubits)
    state = state/np.linalg.norm(state)
    backend = FakeCairoV2()
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=3)
    pass_manager.draw(filename="pass_manager.png")
    qc = qk.QuantumCircuit(num_qubits)
    qc.initialize(state, range(num_qubits))
    qc= pass_manager.run(qc, callback=callback_func)
    # pick fisrt 5 passes with the most time
    excute_info = sorted(excute_info, key=lambda x: x[1], reverse=True)
    print(f"num_qubits: {num_qubits}")
    print(excute_info[:5])

