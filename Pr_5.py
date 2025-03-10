import numpy as np

class NeuralNetwork:
    def __init__(self, input_neurons, hidden_neurons, output_neurons):
        self.input_neurons = input_neurons
        self.hidden_neurons = hidden_neurons
        self.output_neurons = output_neurons

        self.weights_input_hidden = np.random.uniform(-1, 1, (self.input_neurons, self.hidden_neurons))
        self.bias_hidden = np.random.uniform(-1, 1, (1, self.hidden_neurons))
        self.weights_hidden_output = np.random.uniform(-1, 1, (self.hidden_neurons, self.output_neurons))
        self.bias_output = np.random.uniform(-1, 1, (1, self.output_neurons))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, X):
        self.hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.hidden_output = self.sigmoid(self.hidden_input)
        self.output_input = np.dot(self.hidden_output, self.weights_hidden_output) + self.bias_output
        self.output = self.sigmoid(self.output_input)
        return self.output

    def backward(self, X, y, output, learning_rate):
        error = y - output
        d_output = error * self.sigmoid_derivative(output)
        d_hidden_output = np.dot(d_output, self.weights_hidden_output.T)
        d_hidden_input = d_hidden_output * self.sigmoid_derivative(self.hidden_output)

        self.weights_hidden_output += np.dot(self.hidden_output.T, d_output) * learning_rate
        self.bias_output += np.sum(d_output, axis=0, keepdims=True) * learning_rate
        self.weights_input_hidden += np.dot(X.T, d_hidden_input) * learning_rate
        self.bias_hidden += np.sum(d_hidden_input, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output, learning_rate)
            loss = np.mean(np.square(y - output))
            if epoch % 100 == 0:
                print(f'Epoch {epoch}, Loss: {loss}')

        print("Weights and Biases after training:")
        print("Weights Input-Hidden:")
        print(self.weights_input_hidden)
        print("Bias Hidden:")
        print(self.bias_hidden)
        print("Weights Hidden-Output:")
        print(self.weights_hidden_output)
        print("Bias Output:")
        print(self.bias_output)

# XOR dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Initialize and train the neural network
nn = NeuralNetwork(input_neurons=2, hidden_neurons=3, output_neurons=1)
nn.train(X, y, epochs=10000, learning_rate=0.1)

# Test the trained network
print("Predictions after training:")
print(nn.forward(X))
