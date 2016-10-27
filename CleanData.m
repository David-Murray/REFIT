function [DataTable, CleaningData] = CleanData(DataTable)
%CLEANDATA Summary of this function goes here
%   Detailed explanation goes here
%X = House_12_D.Time > House_12_A.Time(end);
%House_12_Complete = [House_12_A; House_12_D(X,:);];
DataTable.Unix = posixtime(DataTable.Time);
DataTable = DataTable(:,[1 12 2:11]);
CleaningData = table();
[DataTable, CleaningData] = GapFilling(DataTable, CleaningData);
[DataTable, CleaningData]= SpikeRemoval(DataTable, CleaningData);
end

