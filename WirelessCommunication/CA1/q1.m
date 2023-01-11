%% A)

% SNR
SNR_db = 0:2:20;
SNR = 10.^(SNR_db/10);

% Symbol creation
M = 2; % PSK order
num_symbol = 1e6;
N = 10; %Number of repeats per SNR
%Outer loop (loop on different SNR values)
error_ = zeros(length(SNR), 1);
for i=1:length(SNR)
    % Inner loop (calculating error for a large number of times(N) and
    % averaging rates.
    num_error = 0;
    for j=1:N
        symbols = randi([0, M-1], num_symbol, 1);
        x_modulated = pskmod(symbols, M);
        noise_power = 1;
        sigpower = noise_power.*SNR(i);
        x_modulated = x_modulated * sqrt(2*sigpower);
        noise = sqrt(0.5)*(randn(size(x_modulated)) + 1j.*randn(size(x_modulated)));
        % AWGN Channel effect:
        rx_modulated = x_modulated+noise;
        % Demodulation:
        y = pskdemod(rx_modulated, M);
        num_error = num_error + sum(y ~= symbols);
    end
    error_(i) = num_error/N/length(x_modulated);
end
semilogy(SNR_db, error_+eps);
hold on
%% B)
% SNR
SNR_db = 0:2:20;
SNR = 10.^(SNR_db/10);

% Symbol creation
M = 2; % PSK order
num_symbol = 1e6;
N = 20; %Number of repeats per SNR
%Outer loop (loop on different SNR values)
error_ = zeros(length(SNR), 1);
for i=1:length(SNR)
    % Inner loop (calculating error for a large number of times(N) and
    % averaging rates.
    num_error = 0;
    tic
    for j=1:N
        symbols = randi([0, M-1], num_symbol, 1);
        x_modulated = pskmod(symbols, M);
        noise_power = 1;
        sigpower = noise_power.*SNR(i);
        x_modulated = x_modulated * sqrt(2*sigpower);
        noise = sqrt(0.5)*(randn(size(x_modulated)) + 1j.*randn(size(x_modulated)));
        % Channel effect:
        % Flat fading + White gaussian noise:
        h = sqrt(0.5)*(randn(size(x_modulated)) + 1j.*randn(size(x_modulated)));
        rx_modulated = h.*x_modulated+noise;
        % Demodulation:
        y = pskdemod(rx_modulated./h, M);
        num_error = num_error + sum(y ~= symbols);
    end
    toc
    error_(i) = num_error/N/length(x_modulated);
end
semilogy(SNR_db, error_+eps);

%% C
% SNR
SNR_db = 0:2:20;
SNR = 10.^(SNR_db/10);

% Symbol creation
M = 2; % PSK order
num_symbol = 1e6;
N = 20; %Number of repeats per SNR
%Outer loop (loop on different SNR values)
error_ = zeros(length(SNR), 1);
for i=1:length(SNR)
    % Inner loop (calculating error for a large number of times(N) and
    % averaging rates.
    num_error = 0;
    for j=1:N
        symbols = randi([0, M-1], num_symbol, 1);
        x_modulated = pskmod(symbols, M);
        noise_power = 1;
        sigpower = noise_power.*SNR(i);
        x_modulated = x_modulated * sqrt(2*sigpower);
        noise1 = sqrt(0.5)*(randn(size(x_modulated)) + 1j.*randn(size(x_modulated)));
        noise2 = sqrt(0.5)*(randn(size(x_modulated)) + 1j.*randn(size(x_modulated)));
        % Channel effect:
        % Flat fading + White gaussian noise:
        h1 = sqrt(0.5)*(randn(size(x_modulated)) + 1j.*randn(size(x_modulated)));
        h2 = sqrt(0.5)*(randn(size(x_modulated)) + 1j.*randn(size(x_modulated)));
        rx_modulated1 = h1.*x_modulated+noise1;
        rx_modulated2 = h2.*x_modulated+noise2;
        rx_eq = (conj(h1).*rx_modulated1 + conj(h2).*rx_modulated2)./(abs(h1).^2+abs(h2).^2);
        % Demodulation:
        y = pskdemod(rx_eq, M);
        num_error = num_error + sum(y ~= symbols);
    end
    error_(i) = num_error/N/length(symbols);
end

semilogy(SNR_db, error_+eps);
