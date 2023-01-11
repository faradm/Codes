np.random.seed(364)
N = 25
n = 2
# Sigma is the true covariance
Sigma = np.random.uniform(size=(n, n))
Sigma = (1 / 2) * (Sigma + Sigma.T)
Sigma = Sigma + n * np.eye(n)
# mu is the true mean
temp_mu = np.random.uniform(size=(n, 1))
res = np.linalg.inv(Sigma) @ temp_mu
res = np.maximum(res, 0)
mu = (Sigma @ res).reshape((n,))
323
# X is drawn from Normal(mu, Sigma_
X = np.random.multivariate_normal(mean=mu, cov=Sigma, size=N)
