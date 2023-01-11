function [d, num_in_queue, num_in_system] = hw2_b(lmbd)
    m = 10;
    u = 5;
    lambda = lmbd;
    n = 100000;
    %inter arrival times are exponential:generate n exp distributed numbers
    %with param (m*lambda):
    inter_arrival = exprnd(1/(m*lambda(1)), n, 1);
    arrival_time = cumsum(inter_arrival);
    %Service time are exponentially distributed, gen n service time with param
    %m*mu:
    service_time = zeros(m, n);
    for i=1:m
        service_time(i, :) = exprnd(1/u, n, 1);
    end
    delta = 0.0001;
    number_time_steps = ceil(max(arrival_time)/delta);
    num_in_system = zeros(number_time_steps, 1);
    num_in_queue = zeros(number_time_steps, 1);
    num_in_server = zeros(number_time_steps, m);
    S = zeros(m, 1);
    Q = 0;
    i = 0;
    remaining_time = zeros(m, 1);
    departured_customers = 0;
    enter_exit = -1*ones(n, 2);
    for t=(1:number_time_steps)
        num_in_system(t) = Q + sum(S);
        num_in_queue(t) = Q;
        num_in_server(t,:) = S;
        %customer exit system
        for server=1:m
            if S(server) == 1
                remaining_time(server) = remaining_time(server) - delta;
                if remaining_time(server) <= 0
                    enter_exit(departured_customers+1, 2) = t*delta;
                    departured_customers = departured_customers + 1;
                    S(server) = 0;
                end
            end
        end
        %customers enter servers from queue
        while Q > 0 && sum(S) < 10
            Q = Q - 1;
            server = find(S==0, 1, 'first');
            S(server) = 1;
            remaining_time(server) = service_time(server, departured_customers+1);
        end
        %customer enter system
        while i+1 < n && arrival_time(i+1) < t*delta
            if sum(S) < 10
                server = find(S==0, 1, 'first');
                S(server) = S(server) + 1;
                remaining_time(server) = service_time(departured_customers+1);
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