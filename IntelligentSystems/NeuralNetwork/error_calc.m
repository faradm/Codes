function [e] = error_calc(pred, output)
    e = 0;
    for i=1:size(pred, 1)
        if(~isequal(pred(i, :), output(i, :)))
            e = e + 1;
        end
    end
    e = e / size(pred,1);
end