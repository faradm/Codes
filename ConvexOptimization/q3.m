%%
min_time_speed_data

%% 

cvx_begin
variables t(N+1) f(N)

minimize ( d*sum(inv_pos(sqrt(t(1:N)))) )

subject to:
    1/(2*eta)*m*t(1) + sum(f) + d*sum(inv_pos(sqrt(t(1:N))))*P/eta <= F;
    t >= 0;
    for i=1:N
        f(i) == 1/eta*( 1/2*m*t(i+1) +m*g*h(i+1) - m*g*h(i) - 1/2*m*t(i) + d*C_D*t(i) );
    end
    f >= 0;
cvx_end
sprintf("Optimum time: %f\n", cvx_optval)
%% Constant fuel:
cvx_begin
variables tc(N+1)

minimize ( d*sum(inv_pos(sqrt(tc(1:N)))) )

subject to:
    (N+1)*1/(2*eta)*m*tc(1) + d*sum(inv_pos(sqrt(tc(1:N))))*P/eta <= F;
    tc >= 0;
    for i=1:N
        1/(2*eta)*m*tc(1) == 1/eta*( 1/2*m*tc(i+1) +m*g*h(i+1) - m*g*h(i) - 1/2*m*tc(i) + d*C_D*tc(i) );
    end
cvx_end
sprintf("Constant fuel time: %f\n", cvx_optval)
%%
s = sqrt(t); % minimum time speed
sc = sqrt(tc); % constant fuel speed
f = [1/(2*eta)*m*t(1);f]; % minimum time fuel burn
fc = 1/(2*eta)*m*tc(1)*ones(N+1,1); % constant fuel fuel burn.

figure
subplot(3,1,1)
plot((0:N)*d,h);
ylabel('height');
subplot(3,1,2)
stairs((0:N)*d,s,'b');
hold on
stairs((0:N)*d,sc,'--r');
legend('minimum time','constant burn')
ylabel('speed')
subplot(3,1,3)
plot((0:N)*d, f,'b');
hold on
plot((0:N)*d, fc,'--r')
xlabel('distance')
ylabel('fuel used')