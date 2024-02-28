#Universidad del Valle de Guatemala
#Algoritmos y estructura de datos
#Hoja de trabajo 5
#Genser Andree Catalan - 23401

import simpy
import random
import statistics

class Simulation:
    #Metodo para definir los atrivutos
    def __init__(self, env, num, memory, instructions, ram, finish_times):
        self.env = env
        self.num = num
        self.memory = memory
        self.instructions = instructions
        self.ram = ram
        self.finish_times = finish_times
        self.action = env.process(self.processes(self.env, self.memory, self.instructions))

    #Metodo para definir los procesos
    def processes(self, env, memory, instructions):
        global completed_processes
        with self.ram.get(memory) as req:
            yield req
            print(f"Nuevo proceso {numproc} entró a ready a las {env.now:7.4f} y se le asignó {memory} en la RAM")
        
        #Ejecutar instrucciones
        start_time = env.now
        while instructions > 0:
            i = 0
            bo = True
            while i < instructions and i < 3:
                print(f"Proceso {numproc} tiene {instructions} instrucciones y lleva {env.now:7.4f}")
                instructions -= 1
                i += 1
                yield env.timeout(1)
                if instructions == 0:
                    completed_processes += 1
                    print(f'{env.now}: Proceso {numproc} ha terminado a las {env.now:7.4f}')
                    self.ram.put(memory)
                    bo = False
                    break
            if bo:
                flag = random.randint(1, 2)
                if flag == 1:  # Entra en espera
                    print(f'Proceso {numproc} entró en espera')
                    yield env.timeout(1)  
                    print(f'Proceso {numproc} terminó los procesos I/O')
                elif flag == 2:  # Sigue
                    print(f'Proceso {numproc} entró a ready a las {env.now:7.4f}')

        self.finish_times.append(env.now - start_time)

#Metodo main para el menu
def main():
    interval = random.expovariate(1/1)
    random.seed(100)
    env = simpy.Environment()
    cpu = simpy.Resource(env, capacity=3)
    ram = simpy.Container(env, init=100, capacity=100)
    global completed_processes
    completed_processes = 0
    global numproc
    numproc = 0
    finish_times = []

    nprocesses = input("Ingrese la cantidad de procesos a simular: ")
    if nprocesses.isnumeric():
        proc = env.process(new_process(env, interval, nprocesses, ram, finish_times))
        env.run(until=proc)

    #Funcion para calcular la desviacion estandar y promedio
    total_time = sum(finish_times)
    average_time = total_time / len(finish_times)
    std_deviation = statistics.stdev(finish_times)

    print(f"Tiempo promedio total: {average_time}")
    print(f"Desviación estándar: {std_deviation}")

#Metodo para añadirle un nuevo valor a cada proceso
def new_process(env, interval, nprocesses, ram, finish_times):
    global completed_processes
    global numproc
    numproc = 0
    for i in range(int(nprocesses)):
        yield env.timeout(interval)
        numproc += 1
        memory = random.randint(1, 10)
        instructions = random.randint(1, 10)
        if ram.level >= memory:
            print(f"Proceso {numproc} inició a las {env.now:7.4f}")
            Simulation(env, numproc, memory, instructions, ram, finish_times)
            yield env.timeout(1)
        else:
            print(f'{env.now}: No hay suficiente memoria RAM disponible para el proceso {numproc}.')

#Output del main
if __name__ == "__main__":
    main()
