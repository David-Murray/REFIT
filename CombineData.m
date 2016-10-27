function [DataTable, CleaningData] = CombineData(House_A, House_D)
%COMBINEDATA This function combines data from D's and A's Database

% Remove duplicates from A's database.
House_A_w = unique(House_A);
[~,e,~] = unique(House_A_w.Time);
House_A_w = House_A_w(e,:);


% Correct day light savings for first houses. UNix time is in CET
C2013 = (House_A_w.Time > datetime(2013,03,31)) & (House_A_w.Time < datetime(2013,10,27));
C2014 = (House_A_w.Time > datetime(2014,03,30)) & (House_A_w.Time < datetime(2014,10,26));
C2015 = (House_A_w.Time > datetime(2015,03,29)) & (House_A_w.Time < datetime(2015,10,25));
House_A_w.Time(C2013) = House_A_w.Time(C2013)-hours(1);
House_A_w.Time(C2014) = House_A_w.Time(C2014)-hours(1);
House_A_w.Time(C2015) = House_A_w.Time(C2015)-hours(1);

% Combine data where House_A end and House_D can continue
House_D_w = House_D;
X = House_D_w.Time > House_A_w.Time(end);
House_Complete = [House_A_w; House_D_w(X,:);];

% Find if there is data that has been missed.
K = [House_A_w.Time; House_D_w.Time];
x = diff(K);
y = find(x > days(0.25));
z = {K(y) days(K(y+1)-K(y)) K(y+1)};
A = z{:,1};
B = z{:,3};
% Checks if the gaps can be filled by one of the databases
for gap = 1:length(A)
	y = House_A_w.Time >= A(gap) & House_A_w.Time <= B(gap);
	z = House_D_w.Time >= A(gap) & House_D_w.Time <= B(gap);
	asize = sum(y);
	dsize = sum(z);
	if asize > dsize
		display('Use A');
		if exist('Add') == 1
			Add = [Add; House_A_w(y,:)];
		else
			Add = House_A_w(y,:);
		end
	else
		display('Use D');
		if exist('Add') == 1
			Add = [Add; House_D_w(z,:)];
		else
			Add = House_D_w(z,:);
		end
	end
end
[C,~,~] = unique(Add,'rows');
House_Complete = [House_Complete; C;];
[C,~,~] = unique(House_Complete,'rows');
sortrows(C,'Time','ascend');
[~,h,~] = unique(C.Time);
Complete = C(h,:);
[DataTable, CleaningData] = CleanData(Complete);
end