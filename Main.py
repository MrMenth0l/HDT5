import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 42
INTERVALOS = [10, 5, 1]
NUM_PROCESOS = [25, 50, 100, 150, 200]

RAM_CAPACIDAD = 100
CPU_VELOCIDAD = 3
NUM_CPUS = 1

def proceso(env, nombre, ram, cpu, tiempo_llegada):
    global tiempos_totales
    llegada = env.now
    memoria_requerida = random.randint(1, 10)
    instrucciones_pendientes = random.randint(1, 10)

    with ram.get(memoria_requerida) as req:
        yield req
        tiempo_inicio = env.now

        while instrucciones_pendientes > 0:
            with cpu.request() as req_cpu:
                yield req_cpu

                ejecutadas = min(instrucciones_pendientes, CPU_VELOCIDAD)
                yield env.timeout(1)
                instrucciones_pendientes -= ejecutadas

                if instrucciones_pendientes > 0:
                    if random.randint(1, 21) == 1:
                        yield env.timeout(1)

        ram.put(memoria_requerida)
        tiempos_totales.append(env.now - llegada)

