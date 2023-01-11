function [idx] = knearest_neighbors(first_point, all_points, k, type, varargin)
    points_size = size(all_points);
    number_of_points = points_size(1);
    f_point_extended = repmat(first_point, number_of_points, 1);
    if strcmp(type, 'norm1')
        d = sum(abs(f_point_extended - all_points), 2);
    elseif strcmp(type, 'norm2')
        d = sqrt(sum((f_point_extended - all_points).^2, 2));
    elseif strcmp(type, 'normq')
        if(size(varargin) < 1)
            error('not enough parameters provided');
        end
        q = cell2mat(varargin(1));
        d_p = sum((f_point_extended - all_points).^q, 2);
        d = d_p.^(1/q);
    else
        error('Non-recognized distance funciton')
    end
    [~, idx] = sort(d, 'ascend');
    idx = idx(1:k);
end