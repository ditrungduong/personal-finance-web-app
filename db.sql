-- Switch to the personal_finance_db database
USE personal_finance_db;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS income;
DROP TABLE IF EXISTS expense;

-- Create the income table
CREATE TABLE income (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    date DATE NOT NULL
);

-- Create the expense table
CREATE TABLE expense (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    date DATE NOT NULL
);

-- Insert initial data into the income table
INSERT INTO income (source, amount, date) VALUES
    ('Salary', 5000, '2024-01-01'),
    ('Freelance', 1200, '2024-01-10'),
    ('Investment', 800, '2024-01-15'),
    ('Gift', 200, '2024-01-20');

-- Insert initial data into the expense table
INSERT INTO expense (category, amount, date) VALUES
    ('Rent', 1500, '2024-01-05'),
    ('Groceries', 300, '2024-01-08'),
    ('Utilities', 200, '2024-01-10'),
    ('Transportation', 100, '2024-01-12'),
    ('Entertainment', 150, '2024-01-18');
