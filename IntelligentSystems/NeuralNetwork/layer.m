function [zb, z] = layer(X, W, active_func)
    zb = X*W;
    z = active_func(zb);
end