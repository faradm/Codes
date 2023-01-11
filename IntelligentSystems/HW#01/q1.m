train_data = load('HW#01_Datasets\Bayesian\data_test.mat');
test_data = load('HW#01_Datasets\Bayesian\data_test.mat');
train_data = train_data.data_test;
test_data = test_data.data_test;
n_train = length(train_data(:, 6));
n_test = length(test_data(:, 6));
%% 1-1
ill_data = train_data(train_data(:, 6) == 1, :);
healthy_data = train_data(train_data(:, 6) == 0, :);
n_s_smpl = length(ill_data(:, 6));
pc1 = n_s_smpl/n_train;
pc0 = 1-pc1;
%% 1-2
%PART A: Calculating params
%Healthy class: C0
%Ill class: C1
%mean ~ eta, sigma ~ std
eta_healthy = mean(healthy_data(:, 1:5));
sigma_healthy = std(healthy_data(:, 1:5));
eta_ill = mean(ill_data(:, 1:5));
sigma_ill = std(ill_data(:, 1:5));
%PART B: Classifing test data
P = @(eta,sigma, x) 1./sqrt(2*pi.*sigma.^2).*exp(-(x-eta).^2./(2*(sigma.^2))); 
eta_h_extended = repmat(eta_healthy, n_test, 1);
sigma_h_extended = repmat(sigma_healthy, n_test, 1);
eta_i_extended = repmat(eta_ill, n_test, 1);
sigma_i_extended = repmat(sigma_ill, n_test, 1);
pc0givx = pc0 * prod(P(eta_h_extended, sigma_h_extended, test_data(:, 1:5)), 2);
pc1givx = pc1 * prod(P(eta_i_extended, sigma_i_extended, test_data(:, 1:5)), 2);
is_ill_hyp = (pc1givx > pc0givx);
is_ill = test_data(:, 6);
accuracy = sum(is_ill_hyp == is_ill)/n_test;