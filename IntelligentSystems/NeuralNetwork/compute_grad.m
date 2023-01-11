function [grad] = compute_grad(X, w, y, regularization, lambda)
    m = length(X(:, 1));
    f_n = length(X(1, :));
    l = repmat(1./(1+exp(X*w)), 1, f_n);
    r = repmat(1./(1+exp(-X*w)), 1, f_n);
    y_expanded = repmat(y, 1, f_n);
    C = y_expanded.*X .* (l+r)-X.*r;
    if regularization == 0
        grad = -sum(C)/m;
    else
        grad = -sum(C)/m + lambda.*w';
    end
end