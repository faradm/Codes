%%
simple_portfolio_data

opt_risk_uni = x_unif'*S*x_unif;
%% No other constraint:
cvx_begin
variable x(n)

minimize(-pbar'*x+ x'*S*x)

pbar'*x == sum(pbar)/n;
sum(x) == 1;
cvx_end

opt_risk_no = x'*S*x;
%% Long only:

cvx_begin
variable x(n)

minimize(-pbar'*x+ x'*S*x)

pbar'*x == sum(pbar)/n;
x >= 0;
sum(x) == 1;
cvx_end
opt_risk_long = x'*S*x;
%% Limited short position:

cvx_begin
variable x(n)

minimize(-pbar'*x+ x'*S*x)

pbar'*x == sum(pbar)/n;
norm(x, 1) <= 2;
sum(x) == 1;
cvx_end
opt_risk_limited = x'*S*x;

%%
sprintf("unconstrained risk:%f\n", opt_risk_no)
sprintf("long only risk:%f\n", opt_risk_long)
sprintf("limited short risk:%f\n", opt_risk_limited)
%% b-1) limited short position:
mu = logspace(-3, 3, 100);
history_optval1 = zeros(100, 1);
history_var1    = zeros(100, 1);
history_x1      = zeros(n, 100);

for i=1:100
   
    cvx_begin quiet
    variable x(n)

    minimize(-pbar'*x+ mu(i)*quad_form(x, S))
    norm(x, 1) <= 2;
    sum(x) == 1;
    cvx_end
    history_x1(:, i) = x;
    history_var1(i) = x'*S*x;
    history_optval1(i) = pbar'*x;
end

%% b-2)

history_optval2 = zeros(100, 1);
history_var2    = zeros(100, 1);
history_x2      = zeros(n, 100);

for i=1:100
   
    cvx_begin quiet
    variable x(n)

    minimize(-pbar'*x+ mu(i)*quad_form(x, S))
    x >= 0;
    sum(x) == 1;
    cvx_end
    history_x2(:, i) = x;
    history_var2(i) = x'*S*x;
    history_optval2(i) = pbar'*x;
end

%%
figure()
hold on
plot(sqrt(history_var1), history_optval1)
plot(sqrt(history_var2), history_optval2)
legend(["Limited short", "long only"]);
xlabel("std");
ylabel("Expected Profit")