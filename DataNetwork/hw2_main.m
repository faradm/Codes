lambda = [4, 4.5, 4.7, 4.8, 4.9];

mean_d_a = zeros(size(lambda));
mean_n_system_a = zeros(size(lambda));

mean_d_b = zeros(size(lambda));
mean_n_system_b = zeros(size(lambda));

mean_d_c = zeros(size(lambda));
mean_n_system_c = zeros(size(lambda));

for i = 1:length(lambda)
    lmbd = lambda(i);
    [d_a, num_in_queue_a, num_in_system_a] = hw2_a(lmbd);
    [d_b, num_in_queue_b, num_in_system_b] = hw2_b(lmbd);
    [d_c, num_in_queue_c, num_in_system_c] = hw2_c(lmbd);

    mean_d_a(i) = mean(d_a);
    mean_n_system_a(i) = mean(num_in_system_a);

    mean_d_b(i) = mean(d_b);
    mean_n_system_b(i) = mean(num_in_system_b);

    mean_d_c(i) = mean(d_c);
    mean_n_system_c(i) = mean(num_in_system_c);
end
figure();
hold on;
plot(lambda, mean_d_a);
plot(lambda, mean_d_b);
plot(lambda, mean_d_c);
legend(["M/m/1", "M/m/m", "M/G/1"])
ylabel("End to end delay");
xlabel("Lambda");
hold off
figure()
hold on
plot(lambda, mean_n_system_a);
plot(lambda, mean_n_system_b);
plot(lambda, mean_n_system_c);
legend(["M/m/1", "M/m/m", "M/G/1"])
ylabel("Number of customers in system");
xlabel("Lambda");
hold off