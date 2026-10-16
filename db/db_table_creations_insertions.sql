CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- 1. Table: books
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    total_copies INT NOT NULL,
    available_copies INT NOT NULL CHECK(available_copies >= 0)
);

-- 2. Table: members
CREATE TABLE IF NOT EXISTS members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    join_date DATE NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active'
);

-- 3. Table: book_issues
CREATE TABLE IF NOT EXISTS book_issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Insert some sample data to get started
INSERT INTO books (title, author, category, total_copies, available_copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 5, 5),
('1984', 'George Orwell', 'Dystopian', 3, 3),
('To Kill a Mockingbird', 'Harper Lee', 'Classic', 4, 4),
('Clean Code', 'Robert C. Martin', 'Technology', 2, 2);

INSERT INTO members (name, email, join_date, status) VALUES
('Alice Smith', 'alice@example.com', '2023-01-15', 'active'),
('Bob Johnson', 'bob@example.com', '2023-05-20', 'active'),
('Charlie Brown', 'charlie@example.com', '2024-02-10', 'active');

INSERT INTO books (title, author, category, total_copies, available_copies) 
VALUES 
    ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 4, 4),
    ('Dune', 'Frank Herbert', 'Science Fiction', 6, 6),
    ('Pride and Prejudice', 'Jane Austen', 'Romance', 3, 3),
    ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 5, 5),
    ('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Non-Fiction', 7, 7),
    ('Atomic Habits', 'James Clear', 'Self-Help', 10, 10),
    ('The Pragmatic Programmer', 'Andrew Hunt', 'Technology', 2, 2),
    ('Thinking, Fast and Slow', 'Daniel Kahneman', 'Psychology', 4, 4);

-- Insert a bunch of members
INSERT INTO members (name, email, join_date, status) 
VALUES 
    ('Diana Prince', 'diana.prince@example.com', '2023-08-12', 'active'),
    ('Clark Kent', 'clark.kent@example.com', '2023-09-01', 'active'),
    ('Bruce Wayne', 'bruce.wayne@example.com', '2023-10-15', 'active'),
    ('Barry Allen', 'barry.allen@example.com', '2024-01-05', 'active'),
    ('Hal Jordan', 'hal.jordan@example.com', '2024-02-20', 'inactive'),
    ('Arthur Curry', 'arthur.curry@example.com', '2024-03-11', 'active'),
    ('Victor Stone', 'victor.stone@example.com', '2024-04-02', 'active');
