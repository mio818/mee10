CREATE DATABASE if not exists happyDB;

-- USE happyDB;

-- -- | id | point | user_id | created_at | updated_at | 
-- -- | user_id | user_name | user_discord_id | created_at | updated_at |

-- CREATE TABLE users(
--     user_discord_id BIGINT NOT NULL,
--     user_name VARCHAR(255) NOT NULL,
--     created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--     PRIMARY KEY (user_discord_id)
-- );

-- CREATE TABLE points(
--     id INT NOT NULL AUTO_INCREMENT,
--     point INT NOT NULL DEFAULT 0,
--     user_id BIGINT NOT NULL,
--     created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--     PRIMARY KEY (id),
--     FOREIGN KEY (user_id) REFERENCES users(user_discord_id) ON DELETE CASCADE
-- )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
