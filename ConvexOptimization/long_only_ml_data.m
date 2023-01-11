n = 20;
rng(0)
%Sigma is the true covariance - PSD
Sigma = rand(n, n);
Sigma = 0.5*(Sigma + Sigma');
Sigma = Sigma + n*eye(n);
% Res = (Sigma^{-1} temp_mu)_+
% Designed so that there are some zero entries
temp_mu = rand(n,1);
res = Sigma \ temp_mu;
res = max(res, 0);
% Compute implied mu
mu = Sigma*res;
% Draw N random samples from distribution
N = 25;
X = randn(n, N);
MU = zeros(n, N);
for i = 1:N
MU(:,i) = mu;
end
Sq = sqrtm(Sigma);
X = Sq*X;
X = X + MU;
