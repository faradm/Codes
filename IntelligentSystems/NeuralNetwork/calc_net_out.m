function [y_pred] = calc_net_out(X, W1, b1, W2, b2, activation_func, discrete)
    yh = activation_func(X*W1+b1);
    yp = activation_func(yh*W2+b2);
    y_pred = yp;
    if(discrete == 1)
        y_pred = yp >= 0.5;
    end
end