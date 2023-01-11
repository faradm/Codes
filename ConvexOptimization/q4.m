%%
morphing_data

%% Euclidian
p_i = q + (0:N-1)'*(r-q)./(N-1);

%% Hellinger

%% Kolmogorov

cvx_begin
variable z(N, n) nonnegative

minimize( sum( max(abs(cumsum(z(1:N-1, :), 2)- cumsum(z(2:end, :),2)),[], 2) ) )

subject to:
    sum(z, 2) == ones(N, 1);
    z(1, :) == q;
    z(N, :) == r;
cvx_end
%% Plot Kolmogorov
figure()
plot(z');
legend(["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]);

%% Plot Euclidian
figure()
plot(p_i');
legend(["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10"]);