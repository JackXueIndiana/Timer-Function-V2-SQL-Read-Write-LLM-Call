CREATE TABLE SalesLT.MarketStatement (
    [MarketStatementId] INT IDENTITY(1,1) PRIMARY KEY,
    [ProductID] INT,
    [Status] NVARCHAR(1000) NOT NULL,
    [Statement] NVARCHAR(1000) NOT NULL
);
