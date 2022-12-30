from Pyro4 import expose
import math


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.initial_number = None
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

        self.base = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        self.initial_number = self.read_input()
        s = int(math.sqrt(self.initial_number))
        step = int((self.initial_number - s) / len(self.workers))
        factors = []
        for i in range(0, len(self.workers)):
            start = i * step + s
            end = s + (i + 1) * step
            factors.append(self.workers[i].factor(start, end, self.initial_number, self.base))

        self.write_output(factors)

    def read_input(self):
        f = open(self.input_file_name, 'r')
        init_number = int(f.readline())
        return init_number

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            for a in output:
                for i in a.value: f.write(str(i) + ' ')

    @staticmethod
    @expose
    def factor(start, end, n, base):
        pairs = []
        for i in range(start, end):
            for j in range(len(base)):
                lhs = i ** 2 % n
                rhs = base[j] ** 2 % n
                if lhs == rhs:
                    pairs.append([i, base[j]])
        new = []
        for i in range(len(pairs)):
            factor = Solver.gcd(pairs[i][0] - pairs[i][1], n)
            if factor != 1:
                new.append(factor)
        new = list(dict.fromkeys(new))
        new = [str(e) for e in new]
        return new

    @staticmethod
    @expose
    def gcd(a, b):
        if b == 0:
            return a
        else:
            return Solver.gcd(b, a % b)
