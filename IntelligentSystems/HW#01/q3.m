data = load('HW#01_Datasets\KNN\data.mat');
labels = load('HW#01_Datasets\KNN\labels.mat');
data = data.data2;
labels = labels.labels;
data = [data, labels];
data = data(randperm(size(data, 1)), :);%Swap data columns randomly
c = 6; % 6-folded cross validation
data = repmat(data, 1, 1, c);
test_filter_idx = zeros(size(data));
m = length(data(:, 1, 1));
n = length(data(1, :, 1));
m_c = int32(m/c)-1;
m_prime = m - m_c; %% number of train samples after partitioning into test and train
for i=1:c
    test_filter_idx((i-1)*m_c+1:i*m_c, :, i) = ones(m_c, n);
end
train_filter_idx = ones(size(data)) - test_filter_idx;
train  = reshape(data(logical(train_filter_idx)), [m_prime, n, c]);
test = reshape(data(logical(test_filter_idx)), [m_c, n, c]);
X = train(:, 1:4, :);
y = squeeze(train(:, 5, :));
X_test = test(:, 1:4, :);
y_test = squeeze(test(:, 5, :));
s = size(y_test);
K = [3 5 7 9]'; % K nearest neighbors!
det = zeros(s(1), s(2), length(K));
for i = 1:length(K) % Loop on different number of nearest neighbors
    k = K(i);
    for j = 1:c %% Loop on different test sets
        for point = 1:length(X_test(:, 1, j))
            nearest_neighbors = knearest_neighbors(X_test(point, :, j), X(:, :, j), k, 'normq', 5);
            y_hyp = y(nearest_neighbors, j);
            first = sum(y_hyp == 1);
            second = sum(y_hyp == 2);
            third = sum(y_hyp == 3);
            [~, det(point, j, i)] = max([first, second, third]);
        end
        errorkj(i, j) = sum((det(:, j, i) ~= y_test(:, j)))./length(det(:, j, i));
    end
end
errork = sum(errorkj, 2) ./ size(errorkj, 2);
[~, idx] = min(errork);
k_best = K(idx);