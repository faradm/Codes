function [l] = loss_(y_pred, y)
    %l = 1/length(y_pred)*sum((y-y_pred).^2);
    l = 1/length(y_pred).*sum(abs(y-y_pred), 2);
end