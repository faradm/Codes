%% Q2
epsilon = 0:0.01:0.5;
SNR_dB = 5;
rep = 1e4;
M = 2;
N = 64;
mse_ = zeros(size(epsilon));
eps_hatt = zeros(size(epsilon));
%Outer loop (loop on different values of epsilon)
first_sign = 1;
changed_sign = 0;
for i=1:length(epsilon)
    %Inner loop, estimate epsilon different times and calc average
    freq_offset = exp(1j*2*pi*epsilon(i)*(0:2*N-1)./N);
    freq_offset = freq_offset';
    for j=1:rep
        symbols = randi([0, M-1], N, 1);
        x_modulated = pskmod(symbols, M);
        x_ofdm = ifft(x_modulated);
        % AWGN Channel effect:
        rx1_modulated = awgn(x_ofdm, SNR_dB, 'measured');
        rx2_modulated = awgn(x_ofdm, SNR_dB, 'measured');        
        % Demodulation:
        y1_offset = rx1_modulated .* freq_offset(1:N);
        y2_offset = rx2_modulated .* freq_offset(N+1:end);
        Y1_ofdm = fft(y1_offset);
        Y2_ofdm = fft(y2_offset);
        par = sum(imag(Y1_ofdm.*conj(Y2_ofdm)))/sum(real(Y1_ofdm.*conj(Y2_ofdm)));
        eps_hat = atan(par)/(2*pi);
        eps_hatt(i) = eps_hatt(i) + eps_hat;
        mse_(i) = mse_(i) + (epsilon(i)-eps_hat).^2;     
    end
    mse_(i) = mse_(i)/rep;
    eps_hatt(i) = eps_hatt(i)/rep;
end

figure(1)
loglog(epsilon, mse_);
figure(2)
loglog(epsilon, eps_hatt);


%% Q3
eps_ = epsilon(20);
eps_hat = eps_hatt(20);
freq_offset = exp(1j*2*pi*eps_*(0:N-1)./N);


SNR_dB = 0:0.5:10;
SNR = 10.^(SNR_dB/10);

% Symbol creation
M = 2; % PSK order
N = 64;
rep = 1e4; %Number of repeats per SNR

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
        y_ofdm = fft(rx_modulated.*(freq_offset').*(exp(-1j*2*pi*eps_hat*(0:N-1)./N))');
        y = pskdemod(y_ofdm, M);
        num_error = num_error + sum(y ~= symbols);
    end
    error_(i) = num_error/rep/length(x_modulated);
end
semilogy(SNR_dB, error_+eps);