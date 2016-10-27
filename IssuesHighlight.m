function [DataTable] = IssuesHighlight(DataTable)
%% Issue one
% Sum of sub-metering is greater than aggregate.
X = DataTable.Aggregate - (DataTable.Appliance1 + DataTable.Appliance2 + DataTable.Appliance3 + DataTable.Appliance4 + DataTable.Appliance5 + DataTable.Appliance6 + DataTable.Appliance7 + DataTable.Appliance8 + DataTable.Appliance9);
Y = X < 0;
DataTable.Issues = Y*1;
end