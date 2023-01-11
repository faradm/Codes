%%Non-regularized
prob = @(X, w) 1./(1+exp(-X*w)); %% Mapping values to probabilities
loss = @(X, w, y) -1/m * (sum(sum(y.*log(prob(X,w)+eps)+(1-y).*log(1-prob(X,w)+eps)))); %% Loss function
k = 5; %5-folded cross validation
eta = 0.001;%gradient descent step
data = load('HW#01_Datasets\Logistic\data_logistic.mat');
data = data.logistic_data;
m = length(data(:, 1));
n = length(data(1, :)) + 1;%%Features including bias
data = repmat(data, 1, 1, k);
train_filter_idx = zeros(size(data));
for i=1:k
    train_filter_idx((i-1)*m/k+1:i*m/k, :, i) = ones(m/k, n-1);
end
test_filter_idx = ones(size(data)) - train_filter_idx;
train  = reshape(data(logical(test_filter_idx)), [m-m/k, n-1, k]);
test = reshape(data(logical(train_filter_idx)), [m/k, n-1, k]);
m_prime = m - m/k; %% number of train samples after partitioning into test and train
X = [ones(m_prime, 1, k), train(:, 1:2, :)];
y = train(:, 3, :);
y = squeeze(y);
X_test = [ones(m/k, 1, k), test(:, 1:2, :)];
y_test = squeeze(test(:, 3, :));
w = zeros(n-1, k);
loss_ = zeros(100, k);
% Grdient descent:
i = 0;
for kk = 1:k %% Outer loop. At each iteration a different set is choosed as train set. 
    while i<1e5 %% Inner loop, termination condition of gradient descent 
        i = i + 1;
        loss_(i, kk) = loss(X(:, :, kk), w(:, kk), y(:, kk));
        grad = compute_grad(X(:,:, kk), w(:, kk), y(:, kk), 0, 0)';
        delta = eta.*grad;
        w = w - delta;
    end
    %Testing model on test set
    y_hat = X_test(:, :, kk)*w(:, kk) > 0.5;
    prob_true(kk) = 1-sum(abs(y_test(:, kk)-y_hat))/(m/k);
end
w_final = sum(w, 2)/k; %Average weights
prob_avg = sum(prob_true)/length(prob_true);
disp(w_final);
disp(prob_avg);
%% Regularized
prob = @(X, w) 1./(1+exp(-X*w)); %% Mapping values to probabilities
loss = @(X, w, y) -1/m * (sum(sum(y.*log(prob(X,w)+eps)+(1-y).*log(1-prob(X,w)+eps)))); %% Loss function
k = 5; %5-folded cross validation
eta = 0.001;%gradient descent step
data = load('HW#01_Datasets\Logistic\data_logistic.mat');
data = data.logistic_data;
m = length(data(:, 1));
n = length(data(1, :)) + 1;%%Features including bias
data = repmat(data, 1, 1, k);
train_filter_idx = zeros(size(data));
for i=1:k
    train_filter_idx((i-1)*m/k+1:i*m/k, :, i) = ones(m/k, n-1);
end
test_filter_idx = ones(size(data)) - train_filter_idx;
train  = reshape(data(logical(test_filter_idx)), [m-m/k, n-1, k]);
test = reshape(data(logical(train_filter_idx)), [m/k, n-1, k]);
m_prime = m - m/k; %% number of train samples after partitioning into test and train
X = [ones(m_prime, 1, k), train(:, 1:2, :)];
y = train(:, 3, :);
y = squeeze(y);
X_test = [ones(m/k, 1, k), test(:, 1:2, :)];
y_test = squeeze(test(:, 3, :));
w = zeros(n-1, k);
loss_ = zeros(100, k);
% Grdient descent:
i = 0;
lambda = 1;
for kk = 1:k %% Outer loop. At each iteration a different set is choosed as train set. 
    while i<1e5 %% Inner loop, termination condition of gradient descent 
        i = i + 1;
        loss_(i, kk) = loss(X(:, :, kk), w(:, kk), y(:, kk));
        grad = compute_grad(X(:,:, kk), w(:, kk), y(:, kk), 1, lambda)';
        delta = eta.*grad;
        w = w - delta;
    end
    %Testing model on test set
    y_hat = X_test(:, :, kk)*w(:, kk) > 0.5;
    prob_true(kk) = 1-sum(abs(y_test(:, kk)-y_hat))/(m/k);
end
w_final = sum(w, 2)/k; %Average weights
prob_avg = sum(prob_true)/length(prob_true);
disp(w_final);
disp(prob_avg);