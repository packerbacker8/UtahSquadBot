from Matrix import matrix
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def deriv_sigmoid(y):
    return y * (1 - y)
    #return sigmoid(x) * (1 - sigmoid(x))

class neural_network:
    def __init__(self, numInput, numHidden, numOutput):
        self.input_nodes = numInput
        self.hidden_nodes = numHidden
        self.output_nodes = numOutput

        self.learning_rate = 0.1

        self.weights_input_hidden = matrix(self.hidden_nodes, self.input_nodes)
        self.weights_hidden_output = matrix(self.output_nodes, self.hidden_nodes)
        self.weights_input_hidden.randomize(-100,100,1)
        self.weights_input_hidden.map_fn_matrix(lambda x: x / 100)
        self.weights_hidden_output.randomize(-100,100,1)
        self.weights_hidden_output.map_fn_matrix(lambda x: x / 100)

        self.bias_hidden = matrix(self.hidden_nodes, 1)
        self.bias_output = matrix(self.output_nodes, 1)
        self.bias_hidden.randomize(-100,100,1)
        self.bias_hidden.map_fn_matrix(lambda x: x / 100)
        self.bias_output.randomize(-100,100,1)
        self.bias_output.map_fn_matrix(lambda x: x / 100)

    def set_learning_rate(self, rate):
        self.learning_rate = rate
        
    def predict(self, input):
        if not isinstance(input, matrix):
            input = matrix.from_array(input)
        #generating hidden outputs
        hidden = matrix.multiply(self.weights_input_hidden, input)
        hidden.add(self.bias_hidden)
        #activation func
        hidden.map_fn_matrix(sigmoid)
        #generating output's output
        output = matrix.multiply(self.weights_hidden_output, hidden)
        output.add(self.bias_output)
        output.map_fn_matrix(sigmoid)

        return output.to_array()

    def train(self, input_arr, answer_arr):
        input = matrix.from_array(input_arr)
        #generating hidden outputs
        hidden = matrix.multiply(self.weights_input_hidden, input)
        hidden.add(self.bias_hidden)
        #activation func
        hidden.map_fn_matrix(sigmoid)
        #generating output's output
        output = matrix.multiply(self.weights_hidden_output, hidden)
        output.add(self.bias_output)
        output.map_fn_matrix(sigmoid)

        answer = matrix.from_array(answer_arr)

        #caclulate the error Error = answer - output
        output_error = matrix.subtract(answer, output)
        #calculate gradient
        gradients = matrix.map_fn_matrix_static(output, deriv_sigmoid)
        gradients.scale(output_error)
        gradients.scale(self.learning_rate)

        #calculate deltas
        hidden_trans = matrix.transpose(hidden)
        weight_hidden_output_delta = matrix.multiply(gradients, hidden_trans)

        #adjust weights by deltas and bias by gradients
        self.weights_hidden_output.add(weight_hidden_output_delta)
        self.bias_output.add(gradients)

        #calculate hidden layer errors
        weight_hidden_out_trans = matrix.transpose(self.weights_hidden_output)
        hidden_error = matrix.multiply(weight_hidden_out_trans, output_error)
        #calculate hidden gradient
        hidden_gradient = matrix.map_fn_matrix_static(hidden, deriv_sigmoid)
        hidden_gradient.scale(hidden_error)
        hidden_gradient.scale(self.learning_rate)

        #calculate input to hidden deltas
        input_trans = matrix.transpose(input)
        weight_input_hidden_deltas = matrix.multiply(hidden_gradient, input_trans)

        #adjust weights by deltas and bias by gradients
        self.weights_input_hidden.add(weight_input_hidden_deltas)
        self.bias_hidden.add(hidden_gradient)
