from Matrix import matrix
from NeuralNetwork import neural_network
import random
from threading import Event, Thread

nn = neural_network(2,2,1)


def update(interval):
    stopped = Event()
    def loop():
        count = 1
        while not stopped.wait(interval):
            print("cycle={}".format(count))
            count +=1
            print(nn.predict([0,0]))
            print(nn.predict([1,0]))
            print(nn.predict([0,1]))
            print(nn.predict([1,1]))
            print("\n")
    Thread(target=loop).start()
    return stopped.set

mat = matrix(2,3)
mat2 = matrix(3,2)
mat.randomize(3,44)
mat2.randomize(5)
mat2.map_fn_matrix(lambda x: x*-1)
print(mat)
print(mat2)
mat2.scale(1.5)

mat3 = matrix.multiply(m1=mat,m2=mat2)
print(mat3)
mat.transpose_in_place()
print(mat)
mat4 = matrix.transpose(mat2)
print(mat4)

training_data = [{'inputs': [0,0], 'targets':[0]},{'inputs': [1,0], 'targets':[1]},{'inputs': [0,1], 'targets':[1]},{'inputs': [1,1], 'targets':[0]}]

cancel_call_1 = update(0.5)

for i in range(100000):
    x = random.randint(0,len(training_data)-1)
    data = training_data[x]
    nn.train(data['inputs'], data['targets'])

output = nn.predict([0,0])
print(output)
output = nn.predict([0,1])
print(output)
output = nn.predict([1,0])
print(output)
output = nn.predict([1,1])
print(output)

cancel_call_1()
