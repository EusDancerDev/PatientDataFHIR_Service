-- Create staff table
CREATE TABLE IF NOT EXISTS staff (
    index SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    usersurname VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Increased length for argon2 hashes
    role VARCHAR(10) NOT NULL CHECK (role IN ('admin', 'medical'))
);

-- Create index on username and usersurname for faster lookups
CREATE INDEX IF NOT EXISTS idx_staff_name ON staff(username, usersurname); 