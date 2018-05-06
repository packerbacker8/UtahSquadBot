import random
import functools

class matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []

        for row in range(0, self.rows):
            self.data.append([])
            for col in range(0, self.cols):
                self.data[row].append(0)

    def __str__(self):
        mat_str = ''
        for row in range(self.rows):
            mat_str = mat_str + 'Row {}:['.format(row + 1)
            for col in range(self.cols):
                mat_str = mat_str + str(self.data[row][col])
                if col != self.cols - 1:
                    mat_str = mat_str + ','
            mat_str = mat_str + ']\n'
        return mat_str

    @staticmethod
    def from_array(arr):
        result = matrix(len(arr), 1)
        for i in range(len(arr)):
            result.data[i][0] = arr[i]
        return result

    def to_array(self):
        return functools.reduce(lambda rows, cols: rows+cols, self.data)

    def add(self, n):
        if isinstance(n, matrix):
            if n.rows != self.rows or n.cols != self.cols:
                print("Rows and columns must be the same for adding two matricies together.")
                return
            for row in range(self.rows):
                for col in  range(self.cols):
                    self.data[row][col] +=  n.data[row][col]
        elif isinstance(n, int) or isinstance(n, float):
            for row in range(self.rows):
                for col in  range(self.cols):
                    self.data[row][col] +=  n
        else:
            print("Can't add item '{}' of type {} to matrix.".format(n,type(n)))

    @staticmethod
    def subtract(m1, m2):
        if m1.rows != m2.rows or m1.cols != m2.cols:
            print("Rows and columns must match {},{} vs {},{}".format(m1.rows, m1.cols, m2.rows, m2.cols))
            return
        result = matrix(m1.rows, m1.cols)
        for row in range(result.rows):
            for col in  range(result.cols):
                result.data[row][col] = m1.data[row][col] - m2.data[row][col]
        return result

    @staticmethod
    def multiply(m1, m2):
        if isinstance(m1, matrix) and isinstance(m2, matrix):
            #matrix product
            if m2.rows != m1.cols:
                print("Rows of passed in matrix must be equal to columns of matrix applied to.")
                return None
            result = matrix(m1.rows, m2.cols)
            for row in range(result.rows):
                for col in  range(result.cols):
                    #dot product of values in col
                    sum = 0
                    for k in range(m1.cols):
                        sum += m1.data[row][k] * m2.data[k][col]
                    result.data[row][col] = sum
            return result
        else:
            print("Both objects need to be of type matrix")
            return None

    def scale(self, n):
        if isinstance(n, matrix):
            if self.rows != n.rows or self.cols != n.cols:
                print("rows and cols must be the same to scale by element wise matrix values")
                return
            #scale matrix
            for row in range(self.rows):
                for col in  range(self.cols):
                    self.data[row][col] *=  n.data[row][col]
        elif isinstance(n, int) or isinstance(n, float):
            #scale matrix
            for row in range(self.rows):
                for col in  range(self.cols):
                    self.data[row][col] *=  n
        else:
            print("Can't multiply item '{}' of type {} to matrix.".format(n,type(n)))

    def randomize(self, start, stop=0, step=1):
        if stop < start:
            temp = start
            start = stop
            stop = temp
        if step == 0:
            step = 1
        for row in range(self.rows):
            for col in  range(self.cols):
                self.data[row][col] =  random.randrange(start, stop,int(step))

    @staticmethod
    def transpose(m):
        result = matrix(m.cols, m.rows)
        for row in range(result.rows):
            for col in  range(result.cols):
                result.data[row][col] =  m.data[col][row]
        return result

    def transpose_in_place(self):
        result = matrix(self.cols, self.rows)
        for row in range(result.rows):
            for col in  range(result.cols):
                result.data[row][col] =  self.data[col][row]
        self.data = result.data
        self.rows = result.rows
        self.cols = result.cols

    @staticmethod
    def map_fn_matrix_static(mat,function_to_apply):
        if not callable(function_to_apply):
            print("map_fn_matrix requires value passed to be a function")
            return
        result = matrix(mat.rows, mat.cols)
        for row in range(result.rows):
            for col in  range(result.cols):
                result.data[row][col] =  function_to_apply(mat.data[row][col])
        return result

    def map_fn_matrix(self,function_to_apply):
        if not callable(function_to_apply):
            print("map_fn_matrix requires value passed to be a function")
            return
        for row in range(self.rows):
            for col in  range(self.cols):
                self.data[row][col] =  function_to_apply(self.data[row][col])
