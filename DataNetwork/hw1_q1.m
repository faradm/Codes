s = 0;
p0 = 0.1;
p = 0.3;
p1 = [0.35, 0.4, 0.3];
p2 = [0.35, 0.3, 0.4];
n = 10000000; %Number of time steps
number_of_time_visited_s0 = zeros(3, 1);
hist = zeros(n ,1);
for k=1:3
    s = 0;
    for i = 1:n
        r = rand;
        if s == 0
            if r > p0
                s = s + 1;            
            end
        number_of_time_visited_s0(k) = number_of_time_visited_s0(k) + 1;
        elseif s > 0
            if r > p && r <= p + p1(k)
                s = s + 1;
            elseif r > p + p1(k)
                s = s - 1;
            end
        end
        hist(i) = s;
    end
    figure()
    plot(hist)
end
print(number_of_time_visited_s0);