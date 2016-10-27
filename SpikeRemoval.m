function [DataTable,CleaningData] = SpikeRemoval(DataTable, CleaningData)
%SPIKEREMOVAL Zero's values greater than 4kW from IAM readings.
for col = 4:width(DataTable)
    exceedsLimit = DataTable{:,col} > 4000;
    CleaningData.Error(col-2,1) = sum(exceedsLimit);
    DataTable{exceedsLimit,col} = 0;
end
end