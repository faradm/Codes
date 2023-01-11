%% Loading data
train_data = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/train_images.mat');
train_data = double(train_data.train_images);
Y = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/train_lables.mat');
Y = double(Y.train_lables)';
test_data = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/test_images.mat');
test_data = double(test_data.test_images);
Y_test = load('./MNIST dataset fot MATLAB/MNIST dataset fot MATLAB/test_labels.mat');
Y_test = double(Y_test.test_labels);
%% Preprocess
train_data = (train_data - mean(train_data)) ./ (std(train_data)+eps());
test_data = (test_data - mean(test_data)) ./ (std(test_data) + eps());
%% One-hot coding
Y = full(ind2vec(Y'+1))';
Y_test = full(ind2vec(Y_test+1))';
%% Adding 1 feature to data
X = [ones(size(train_data, 1), 1) train_data];
X_test = [ones(size(test_data, 1), 1) test_data];
valid_labels = 0:9;
valid_labels = full(ind2vec(valid_labels+1))';
%% Gradient descent
number_of_epochs = 20;
mini_batch_size = 20;
number_of_iterations = size(X, 1) / mini_batch_size;
learning_rate = 0.0001;
theta = randn(size(X, 2), size(Y, 2)).*0.01;
error_ = zeros(number_of_epochs, 1);
for i=1:number_of_epochs
    for j=1:number_of_iterations
        X_mini_indices = (j-1)*mini_batch_size+1:(j)*mini_batch_size;
        X_batch = X(X_mini_indices, :);
        Y_batch = Y(X_mini_indices, :);
        delta = X_batch' * (X_batch * theta - Y_batch)./mini_batch_size;
        theta = theta - learning_rate .* delta;
    end
    error_(i) = error_calc(X_test*theta >= 0.5, Y_test);
end
plot(1-error_);
%% Closed form formula
theta2 = pinv(X'*X)*X'*Y;
%% Generating output
y_pred2 = X_test * theta2;
y_pred2 = y_pred2 >= 0.5;
y_pred1 = X_test * theta;
y_pred1 = y_pred1 >= 0.5;
error = error_calc(y_pred2, Y_test);
prob_true = 1 - error;

%% Calculating confusion matrix
conf_matrix = zeros(size(valid_labels, 1),size(valid_labels, 1));
for i=1:size(Y_test, 1)
   [~,row]=ismember(Y_test(i, :),valid_labels,'rows');
   [~,col]=ismember(y_pred2(i, :),valid_labels,'rows');
   if(col ~= 0 && row ~= 0)
       conf_matrix(row, col) = conf_matrix(row, col) + 1;
   end
end