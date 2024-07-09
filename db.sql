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

-- Insert data into the income table
INSERT INTO income (source, amount, date) VALUES
    ('Salary', 5000, '2023-07-01'),
    ('Freelance', 1200, '2023-08-10'),
    ('Investment', 800, '2023-09-15'),
    ('Gift', 200, '2023-10-20'),
    ('Salary', 5000, '2023-11-01'),
    ('Freelance', 1300, '2023-12-10'),
    ('Investment', 900, '2024-01-15'),
    ('Gift', 250, '2024-02-20'),
    ('Salary', 5100, '2024-03-01'),
    ('Freelance', 1250, '2024-04-10'),
    ('Investment', 850, '2024-05-15'),
    ('Gift', 300, '2024-06-20'),
    ('Salary', 5200, '2024-07-01'),
    ('Freelance', 1350, '2024-08-10'),
    ('Investment', 950, '2024-09-15'),
    ('Gift', 400, '2024-10-20'),
    ('Salary', 5300, '2024-11-01'),
    ('Freelance', 1400, '2024-12-10');

-- Insert data into the expense table
INSERT INTO expense (category, amount, date) VALUES 
    ('Rent', 1500, '2023-07-05'),
    ('Groceries', 300, '2023-08-08'),
    ('Utilities', 200, '2023-09-10'),
    ('Transportation', 100, '2023-10-12'),
    ('Entertainment', 150, '2023-11-18'),
    ('Rent', 1550, '2023-12-05'),
    ('Groceries', 320, '2024-01-08'),
    ('Utilities', 210, '2024-02-10'),
    ('Transportation', 110, '2024-03-12'),
    ('Entertainment', 160, '2024-04-18'),
    ('Rent', 1600, '2024-05-05'),
    ('Groceries', 330, '2024-06-08'),
    ('Utilities', 220, '2024-07-10'),
    ('Transportation', 120, '2024-08-12'),
    ('Entertainment', 170, '2024-09-18'),
    ('Rent', 1650, '2024-10-05'),
    ('Groceries', 340, '2024-11-08'),
    ('Utilities', 230, '2024-12-10');
