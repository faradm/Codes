%% Loading data
train_data = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/train_images.mat');
train_data = double(train_data.train_images);
%train_labels = train_data;
test_data = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/test_images.mat');
test_data = double(test_data.test_images);
%test_labels = test_data;
%% Defining Parameters
normalization_type = 'maxmin'; %% Or: 'maxmin', 'none'
mini_batch_size = 30;
number_of_iterations = size(train_data, 1)/mini_batch_size;
number_of_epochs = 30;
valid_labels = 0:9;
number_of_hidden_layer_neurons = 256;
gradient_step = 0.01;
momentum = 0;
tanh_ = @(x) tanh(x);
tanh_grad = @(x) 1-tanh_(x).^2;
activation_function = tanh_;
activation_grad = tanh_grad;

%% Preprocess Data
if(strcmp(normalization_type, 'zscore'))
    train_data = (train_data - mean(train_data)) ./ (std(train_data)+eps());
    test_data = (test_data - mean(test_data)) ./ (std(test_data) + eps());
elseif(strcmp(normalization_type, 'maxmin'))
    train_data = (train_data - min(train_data))./ (eps() + (max(train_data) - min(train_data)));
    test_data = (test_data - min(test_data)) ./ (max(test_data)-min(test_data) + eps());
end
test_labels = test_data;
train_labels = train_data;
%% Defining Network structure
W_hidden_layer = randn(size(train_data, 2), number_of_hidden_layer_neurons).*0.01;
b_hidden_layer = zeros(1, number_of_hidden_layer_neurons);
n_out_neuron = size(test_data, 2); %% Number of output nodes
W_output_layer = randn(number_of_hidden_layer_neurons, n_out_neuron).*0.01;
b_output_layer = zeros(1, n_out_neuron);
%% Back-propagation
[W_output_layer, b_output_layer, W_hidden_layer, b_hidden_layer, loss_func, error_epoch] = train_net(train_data, train_labels, test_data, test_labels, gradient_step, mini_batch_size, momentum, number_of_epochs, number_of_iterations, activation_function, activation_grad, W_output_layer, b_output_layer, W_hidden_layer, b_hidden_layer, 0);
% Plotting accuracy and loss
figure(1)
plot(loss_func);

%% Training network with compressed features
X_c = activation_function(train_data * W_hidden_layer + b_hidden_layer);
Y_c = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/train_lables.mat');
Y_c = double(Y_c.train_lables)';
X_ctest = activation_function(test_data * W_hidden_layer + b_hidden_layer);
Y_ctest = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/test_labels.mat');
Y_ctest = double(Y_ctest.test_labels);
Y_c = full(ind2vec(Y_c'+1))';
Y_ctest = full(ind2vec(Y_ctest+1))';

n_out_neuron = size(Y_c, 2); %% Number of output nodes
w1 = randn(size(X_c, 2), 70).*0.01;
b1 = zeros(1, 70);
w2 = randn(70, n_out_neuron).*0.01;
b2 = zeros(1, n_out_neuron);
[w2, b2, w1, b1, loss_func, error_epoch] = train_net(X_c, Y_c, X_ctest, Y_ctest, gradient_step, mini_batch_size, momentum, 40, number_of_iterations, activation_function, activation_grad, w2, b2, w1, b1, 1);
figure(2)
plot(1-error_epoch);
figure(3)
plot(loss_func);