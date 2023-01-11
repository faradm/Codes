%% Loading data
train_data = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/train_images.mat');
train_data = double(train_data.train_images);
train_labels = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/train_lables.mat');
train_labels = double(train_labels.train_lables)';
test_data = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/test_images.mat');
test_data = double(test_data.test_images);
test_labels = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/test_labels.mat');
test_labels = double(test_labels.test_labels);
%% Defining Parameters
normalization_type = 'zscore'; %% Or: 'maxmin', 'none'
mini_batch_size = 30;
number_of_iterations = size(train_data, 1)/mini_batch_size;
number_of_epochs = 20;
valid_labels = 0:9;
number_of_hidden_layer_neurons = 70;
gradient_step = 0.06;
momentum = 0;
sig_ = @(x) 1./(1+exp(-x));
sig_grad = @(x) sig_(x) .* (1-sig_(x));
tanh_ = @(x) tanh(x);
tanh_grad = @(x) 1-tanh_(x).^2;
fx = @(x) x;
fx_grad = @(x)  ones(size(x));
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

%% Defining Network structure
W_hidden_layer = randn(size(train_data, 2), number_of_hidden_layer_neurons).*0.01;
b_hidden_layer = zeros(1, number_of_hidden_layer_neurons);
output_type = 'onehot';
n_out_neuron = []; %% Number of output nodes
if strcmp(output_type, 'binary')
    n_out_neuron = ceil(log2(length(valid_labels)));
    train_labels = dec2bin(train_labels)- '0';
    test_labels = dec2bin(test_labels)- '0';
    valid_labels = dec2bin(valid_labels)- '0';
elseif strcmp(output_type, 'onehot')
    n_out_neuron = length(valid_labels);
    train_labels = full(ind2vec(train_labels'+1))';
    test_labels = full(ind2vec(test_labels+1))';
    valid_labels = full(ind2vec(valid_labels+1))';
end
W_output_layer = randn(number_of_hidden_layer_neurons, n_out_neuron).*0.01;
b_output_layer = zeros(1, n_out_neuron);
%% Back-propagation
error_epoch = zeros(number_of_epochs, 1);
loss_func = zeros(number_of_epochs, 1);
dldw2 = zeros(size(W_output_layer));
dldw1 = zeros(size(W_hidden_layer));
dldb2 = zeros(size(b_output_layer));
dldb1 = zeros(size(b_hidden_layer));
for j=1:number_of_epochs
    for i=1:number_of_iterations
        X_mini_indices = (i-1)*mini_batch_size+1:(i)*mini_batch_size;
        X_batch = train_data(X_mini_indices, :);
        Y_batch = train_labels(X_mini_indices, :);
        %Forward path
        z1 = X_batch*W_hidden_layer+repmat(b_hidden_layer, mini_batch_size, 1);
        yh = activation_function(z1);
        z2 = yh*W_output_layer+repmat(b_output_layer, mini_batch_size, 1);
        yp = activation_function(z2);
        %Backward path, Fully vectorized!
        dldyp = (yp - Y_batch);
        dldz2 = dldyp .* activation_grad(yp);
        dldw2 = momentum.* dldw2 + gradient_step.*(yh' * dldz2)./mini_batch_size;
        dldb2 = momentum .* dldb2 + gradient_step.*sum(dldz2)./mini_batch_size;
        dldyh = dldz2 * W_output_layer';
        dldz1 = activation_grad(yh) .* dldyh;
        dldw1 = momentum.*dldw1 + gradient_step.*(X_batch'*dldz1)./mini_batch_size;
        dldb1 = momentum .* dldb1 + gradient_step.*sum(dldz1)./mini_batch_size;
        %Updating Weights and bias
        W_output_layer = W_output_layer - dldw2;
        W_hidden_layer = W_hidden_layer - dldw1;
        b_output_layer = b_output_layer - dldb2;
        b_hidden_layer = b_hidden_layer - dldb1;
    end
        % Calculating loss and accuracy
        y_pred = calc_net_out(test_data, W_hidden_layer, b_hidden_layer, W_output_layer, b_output_layer, activation_function, 1);
        y_train_p = calc_net_out(train_data, W_hidden_layer, b_hidden_layer, W_output_layer, b_output_layer, activation_function, 1);
        error_epoch(j) = error_calc(y_pred, test_labels);
        loss_func(j) = sum(sum((y_train_p-train_labels).^2));
        disp(error_epoch(j));
end
% Plotting accuracy and loss
figure(1)
plot(1-error_epoch);
figure(2)
plot(loss_func);
%% Calculating confusion matrix
conf_matrix = zeros(size(valid_labels, 1),size(valid_labels, 1));
for i=1:size(test_labels, 1)
   [~,row]=ismember(test_labels(i, :),valid_labels,'rows');
   [~,col]=ismember(y_pred(i, :),valid_labels,'rows');
   if(col ~= 0 && row ~= 0)
       conf_matrix(row, col) = conf_matrix(row, col) + 1;
   end
end
