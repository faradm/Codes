%%
rng("default")
long_only_ml_data

%%
cvx_begin

variable S(n, n) semidefinite
variable z(n)

t = 0;
for i=1:N
   t = t + X(:, i)'*S*X(:, i);
end
maximize(-N*n/2*log(2*pi) + N/2*log_det(S) + sum(X'*z)-N/2*matrix_frac(z, S)-1/2*t)

subject to:
    z >= 0;

cvx_end
sigma1 = inv(S);
mu1 = sigma1*z;

%% Without Constraint
cvx_begin

variable S(n, n) semidefinite
variable z(n)

t = 0;
for i=1:N
   t = t + X(:, i)'*S*X(:, i);
end
maximize(-N*n/2*log(2*pi) + N/2*log_det(S) + sum(X'*z)-N/2*matrix_frac(z, S)-1/2*t)

cvx_end
sigma2 = inv(S);
mu2 = sigma2*z;

%%
sprintf("l2 distance constrained: %f\n", norm(mu1-mu, 2))
sprintf("frobenius constrained: %f\n", norm(sigma1-Sigma, "fro"))

sprintf("l2 distance unconstrained: %f\n", norm(mu2-mu, 2))
sprintf("frobenius unconstrained: %f\n", norm(sigma2-Sigma, "fro"))
