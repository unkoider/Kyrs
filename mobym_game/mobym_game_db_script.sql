CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Players (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id),
    name VARCHAR(50) NOT NULL,
    level INT NOT NULL,
    ads_disabled BOOLEAN NOT NULL,
    donation DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Achievements (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES Players(id),
    name VARCHAR(50) NOT NULL,
    progress INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    purchasable BOOLEAN NOT NULL
);

CREATE TABLE Inventory (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES Players(id),
    item_id INT REFERENCES Items(id),
    quantity INT NOT NULL,
    pregame BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Records (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES Players(id),
    level_name VARCHAR(50) NOT NULL,
    record_t DECIMAL(10, 2) NOT NULL,
    record_s DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert example data
INSERT INTO Users (username, password, is_admin) VALUES 
('user1', '$2b$12$KIX.PLAINuF62YYEz/AgNBOfH1JF0q/J29JF/ir9zzRTtbM987dW3K', FALSE), -- password: password
('user2', '$2b$12$4ETe2vxaOAkl.ZU/EvvHWejPL/DGiB.tg4yOlQzG7mOnVWneW8Sly', FALSE), -- password: password
('admin', '$2b$12$6zqsGixUwrmjbGAxO0/IROa56DxYgLn9VMuLW8XLtG13MIP/gjDba', TRUE);  -- password: admin

INSERT INTO Players (user_id, name, level, ads_disabled, donation) VALUES
(1, 'Player1', 1, FALSE, 50.00),
(2, 'Player2', 2, TRUE, 100.00);

INSERT INTO Achievements (player_id, name, progress) VALUES
(1, 'First Run', 100),
(1, 'Collector', 50),
(2, 'First Run', 100),
(2, 'Speedster', 75);

INSERT INTO Items (name, description, price, purchasable) VALUES
('Double Jump', 'Allows player to jump twice in a row', 10.00, TRUE),
('Magnet', 'Attracts nearby coins', 15.00, TRUE),
('Invincibility', 'Temporarily makes the player invincible', 20.00, FALSE),
('Speed Boost', 'Increases player speed for a short period', 12.00, TRUE);

INSERT INTO Inventory (player_id, item_id, quantity, pregame) VALUES
(1, 1, 2, TRUE),
(1, 2, 1, FALSE),
(2, 3, 1, TRUE);
