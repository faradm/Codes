function [d, num_in_queue, num_in_system] = hw2_c(lmbd)
    m = 10;
    C = 50;
    lambda = lmbd;

    n = 100000;
    %inter arrival times are exponential:generate n exp distributed numbers
    %with param (m*lambda):
    inter_arrival = exprnd(1/(m*lambda(1)), n, 1);
    arrival_time = cumsum(inter_arrival);
    service_time = 1/C*ones(n, 1);
    %delta = min(min(inter_arrival, service_time));
    delta = 0.0001;
    number_time_steps = ceil(max(arrival_time)/delta);
    num_in_system = zeros(number_time_steps, 1);
    num_in_queue = zeros(number_time_steps, 1);
    S = 0;
    Q = 0;
    i = 0;
    remaining_time = 0;
    departured_customers = 0;
    enter_exit = -1*ones(n, 2);
    for t=(1:number_time_steps)
        num_in_system(t) = Q + S;
        num_in_queue(t) = Q;
        %customer exit system
        if S == 1
            remaining_time = remaining_time - delta;
            if remaining_time <= 0
                enter_exit(departured_customers+1, 2) = t*delta;
                departured_customers = departured_customers + 1;
                S = 0;
                if Q > 0
                    Q = Q - 1;
                    S = 1;
                    remaining_time = service_time(departured_customers+1);
                end
            end
        end
        %customer enter system
        while i+1 < n && arrival_time(i+1) < t*delta
            if S == 0
                S = S + 1;
                remaining_time = service_time(departured_customers+1);
            else
                Q = Q + 1;
            end
            enter_exit(i+1, 1) = t*delta;
            i = i + 1;
        end
    end
    d = enter_exit(:, 2) - enter_exit(:, 1);
    last_valid = find(d > 0, 1, 'last'); 
    d = d(1:last_valid);
end