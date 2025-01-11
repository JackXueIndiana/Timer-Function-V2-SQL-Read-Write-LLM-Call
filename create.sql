CREATE TABLE SalesLT.MarketStatement (
    [MarketStatementId] INT IDENTITY(1,1) PRIMARY KEY,
    [ProductId] INT,
    [Statement] NVARCHAR(1000) NOT NULL
);
