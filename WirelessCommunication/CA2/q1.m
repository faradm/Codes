%% A)

% SNR
SNR_dB = 0:0.5:10;
SNR = 10.^(SNR_dB/10);

% Symbol creation
M = 2; % PSK order
N = 64;
rep = 1e5; %Number of repeats per SNR

error_ = zeros(length(SNR), 1);
%Outer loop (loop on different SNR values)
for i=1:length(SNR)
    % Inner loop (calculating error for a large number of times(N) and
    % averaging rates.
    num_error = 0;
    for j=1:rep
        symbols = randi([0, M-1], 64, 1);
        x_modulated = pskmod(symbols, M);
        x_ofdm = ifft(x_modulated);
        % AWGN Channel effect:
        rx_modulated = awgn(x_ofdm, SNR_dB(i), 'measured');
        % Demodulation:
        y_ofdm = fft(rx_modulated);
        y = pskdemod(y_ofdm, M);
        num_error = num_error + sum(y ~= symbols);
    end
    error_(i) = num_error/rep/length(x_modulated);
end
semilogy(SNR_dB, error_+eps);
hold on