function fastfouriertransform(filename)

fid = fopen(filename,'rb');
y = fread(fid,'uint8=>double');

y = y-127.5;
y = (y(1:2:end).^2 + y(2:2:end).^2).^0.5;

X = y;

Y = fft(X);
figure
plot(abs(Y))