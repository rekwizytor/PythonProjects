import time
import numpy as np

class TimeDecorator:
    def __init__(self, func):
        self.func = func
        self.executions_times = []
        self.max = 0
        self.min = 0
        self.mean = 0
        self.std = 0

    def calc_stats(self):
        if len(self.executions_times) == 0:
            return 'Nie wykonano jeszcze funkcji'
        self.max = np.max(self.executions_times)
        self.min = np.min(self.executions_times)
        self.mean = np.mean(self.executions_times)
        self.std = np.std(self.executions_times)

    def __call__(self, *args, **kwargs):
        time_start = time.time()
        result = self.func(*args, **kwargs)
        time_end = time.time()
        execution_time = np.round(time_end - time_start, 4)
        self.executions_times.append(execution_time)
        self.calc_stats()
        print(f'Czas wykonywania funkcji: {execution_time} s')
        return result
    
    def get_stats(self):
        return f'''Statyski funkcji: \n Ilość wykonań: {len(self.executions_times)} \n Czas min: {self.min} s
 Czas max: {self.max} s \n Średni czas: {np.round(self.mean, 4)} s
 Odchylenie standardowe: {np.round(self.std, 4)} s'''

@TimeDecorator
def function(size):
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return np.dot(A, B)


matrix_size = 5000

function(matrix_size)
function(matrix_size)
function(matrix_size)
function(matrix_size)
function(matrix_size)

print(function.get_stats())
