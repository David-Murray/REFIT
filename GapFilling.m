function [DataTable, CleaningData] = GapFilling(DataTable, CleaningData)
%GAPFILLING Fills in data gaps.
%   If a gap is less than two minutes it is filled from previous data, else
%   it is filled with zeros'.
for col = 3:width(DataTable)
    %while(sum(isnan(DataTable{:,col})) ~= 0)
    display([col sum(isnan(DataTable{:,col}))])
    CleaningData.NaNOccurences(col-2,1) = sum(isnan(DataTable{:,col}));
    found = find(isnan(DataTable{:,col}) == 1);
    foundPrevious = found - 1;
    timeCompare = seconds(DataTable{found,1} - DataTable{foundPrevious,1});
    index = timeCompare  > 120;
    CleaningData.NaNOccurencesTime120(col-2,1) = sum(index);
    DataTable{found(index),col} = 0;
    A = DataTable{:,col};
    for ii = 1:size(A,2)
        I = A(1,ii);
        for jj = 2:size(A,1)
            if isnan(A(jj,ii))
                A(jj,ii) = I;
            else
                I  = A(jj,ii);
            end
        end
    end
    DataTable{:,col} = A;
end
end