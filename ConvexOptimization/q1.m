%% Load Data
p_bar = [0.12;0.10;0.07;0.03];
sigma = [0.0064, 0.0008, -0.0011, 0;
         0.0008, 0.0025,  0     , 0;
        -0.0011, 0     ,  0.0004, 0;
         0     , 0     ,  0     , 0;];

%% a)
mu = logspace(0, 7, 100);
history_optval = zeros(100, 1);
history_var = zeros(100, 1);
history_x      = zeros(4, 100);
for i=1:length(mu)
   
    cvx_begin quiet
    variables x(4)
    
    minimize(-p_bar'*x + mu(i)*x'*sigma*x);
    subject to:
        sum(x) == 1;
        x >= 0;
    
    cvx_end
    history_x(:, i) = x;
    history_var(i) = x'*sigma*x;
    history_optval(i) = p_bar'*x;
end

%%
figure()
plot(sqrt(history_var), history_optval)
xlabel("std");
ylabel("Expected Profit")
figure()
hold on
plot(sqrt(history_var), history_x(1, :))
plot(sqrt(history_var), history_x(2, :))
plot(sqrt(history_var), history_x(3, :))
plot(sqrt(history_var), history_x(4, :))
legend(["x1", "x2", "x3", "x4"])
hold off
xlabel("std");
ylabel("Allocation")

%% b
eta = logspace(-4, -1, 100);

history_optval = zeros(100, 1);
history_var = zeros(100, 1);
history_x      = zeros(4, 100);
[Q, D] = eig(sigma);
for i=1:length(eta)
    
    cvx_begin quiet
    variables x(4)
    phi_inv = -sqrt(2)*erfcinv(2*eta(i));
    minimize(-p_bar'*x);
    subject to:
        sum(x) == 1;
        x >= 0;
        phi_inv*norm(sqrt(D)*Q'*x, 2) + p_bar'*x >= 0;
    
    cvx_end
    history_x(:, i) = x;
    history_var(i) = x'*sigma*x;
    history_optval(i) = p_bar'*x;
end

%%
figure()
plot(eta, history_optval)
xlabel("Eta");
ylabel("Expected Profit")
figure()
hold on
plot(eta, history_x(1, :))
plot(eta, history_x(2, :))
plot(eta, history_x(3, :))
plot(eta, history_x(4, :))
legend(["x1", "x2", "x3", "x4"])
hold off
xlabel("Eta");
ylabel("Allocation")