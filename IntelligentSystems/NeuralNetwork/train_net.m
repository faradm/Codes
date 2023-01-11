function [w2, b2, w1, b1, loss_func, error_epoch] = train_net(train_data, train_labels, test_data, test_labels, gradient_step, mini_batch_size, momentum, number_of_epochs, number_of_iterations, activation_function, activation_grad, W_output_layer, b_output_layer, W_hidden_layer, b_hidden_layer, discrete)
error_epoch = zeros(number_of_epochs, 1);
loss_func = zeros(number_of_epochs, 1);
dldw2 = zeros(size(W_output_layer));
dldw1 = zeros(size(W_hidden_layer));
dldb2 = zeros(size(b_output_layer));
dldb1 = zeros(size(b_hidden_layer));
for j=1:number_of_epochs
    for i=1:number_of_iterations
        X_mini_indices = (i-1)*mini_batch_size+1:(i)*mini_batch_size;
        X_batch = train_data(X_mini_indices, :);
        Y_batch = train_labels(X_mini_indices, :);
        %Forward path
        z1 = X_batch*W_hidden_layer+repmat(b_hidden_layer, mini_batch_size, 1);
        yh = activation_function(z1);
        z2 = yh*W_output_layer+repmat(b_output_layer, mini_batch_size, 1);
        yp = activation_function(z2);
        %Backward path, Fully vectorized!
        dldyp = (yp - Y_batch);
        dldz2 = dldyp .* activation_grad(yp);
        dldw2 = momentum.* dldw2 + gradient_step.*(yh' * dldz2)./mini_batch_size;
        dldb2 = momentum .* dldb2 + gradient_step.*sum(dldz2)./mini_batch_size;
        dldyh = dldz2 * W_output_layer';
        dldz1 = activation_grad(yh) .* dldyh;
        dldw1 = momentum.*dldw1 + gradient_step.*(X_batch'*dldz1)./mini_batch_size;
        dldb1 = momentum .* dldb1 + gradient_step.*sum(dldz1)./mini_batch_size;
        %Updating Weights and bias
        W_output_layer = W_output_layer - dldw2;
        W_hidden_layer = W_hidden_layer - dldw1;
        b_output_layer = b_output_layer - dldb2;
        b_hidden_layer = b_hidden_layer - dldb1;
    end
        % Calculating loss and accuracy
        y_pred = calc_net_out(test_data, W_hidden_layer, b_hidden_layer, W_output_layer, b_output_layer, activation_function, discrete);
        y_train_p = calc_net_out(train_data, W_hidden_layer, b_hidden_layer, W_output_layer, b_output_layer, activation_function, discrete);
        error_epoch(j) = error_calc(y_pred, test_labels);
        loss_func(j) = sum(sum((y_train_p-train_labels).^2));
        disp(loss_func(j));
end
w2 = W_output_layer;
b2 = b_output_layer;
w1 = W_hidden_layer;
b1 = b_hidden_layer;
end