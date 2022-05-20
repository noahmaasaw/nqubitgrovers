import qiskit
from qiskit import IBMQ
IBMQ.save_account('2330fa80e6cdc16978c9d943bb82b00665b18d690f370cdc8874f617a1650490dba8b1aa035e152e40a7240c7f626592c9871f4f92d65945b63eb60e85f4a99d')
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
provider = IBMQ.load_account()
import math
import itertools
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, BasicAer

backend = BasicAer.get_backend('qasm_simulator')
shots = 1000

"""n-qubit Grover's algorithm cycling on 4 qubit increments"""    
q=10


def grovers():
    qc = QuantumCircuit(q,q)
    pi = math.pi
    qr = QuantumRegister(q, 'qc')
    qc.add_register(qr)
    qc.qregs

    cr = ClassicalRegister(4 , 'cr')
    qc.add_register(cr)

    #######################
    ######## init #########
    #######################

    for n in range(4):
         qc.h([n])

    #######################
    ### Oracle for 0010 ###
    #######################
    for j in range(4):
             if n != j:
                qc.x([j])
                
    for i in range(0, q-3, 4):
        if n!=0:
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i], qr[i+1])
            qc.cp(-pi/4, qr[i+1], qr[i+3])

            qc.cx(qr[i], qr[i+1])
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])
            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])

            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])

    for j in range(4):
        qc.x([j])

    #######################
    #### Amplification ####
    #######################
    for j in range(4):
        qc.h([j])

    for j in range(4):
        qc.x([j])

    ######## cccZ #########

    for i in range(0, q-3, 4):
        if n!=0:
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i], qr[i+1])
            qc.cp(-pi/4, qr[i+1], qr[i+3])

            qc.cx(qr[i], qr[i+1])
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])
            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])

            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])

    ####### end cccZ #######

    for j in range(4):
        qc.x(qr[j])
    for j in range(4):
        qc.h(qr[j])

    #########################################################
    ####### Measure ON THEORETICAL QUANTUM PROCESSOR ########
    #########################################################

    qc.barrier(qr)
    for i in range(0, q%(q-3), 4):
        qc.measure(qr[i], cr[i])
        qc.measure(qr[i+1], cr[i+1])
        qc.measure(qr[i+2], cr[i+2])
        qc.measure(qr[i+3], cr[i+3])

    # submit job #
    qc.measure_all()
    job = execute(qc, backend, shots=shots)

grovers()
