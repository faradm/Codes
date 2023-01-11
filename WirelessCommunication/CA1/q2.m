%% Channel A
fd1=0.01;
tau1=[0, 0.01e-4];
h1=rayleighchan(1e-4, fd1, tau1, [0 0]);
h1.StoreHistory=1;
y=filter(h1, ones(100, 1));
plot(h1);
%% Channel B
fd2 = 0.01;
tau2 = [0, 5e-4];
h2=rayleighchan(1e-4, fd2, tau2, [0 0]);
h2.StoreHistory=1;
y=filter(h2, ones(100, 1));
plot(h2)

%% Channel C
fd3 = 200;
tau3 = [0, 5e-4];
h3=rayleighchan(1e-4, fd3, tau3, [0 0]);
h3.StoreHistory=1;
y=filter(h3, ones(100, 1));
plot(h3)