-- schema.sql
-- יצירת בסיס נתונים וטבלאות למערכת Workout Manager
-- מיועד ל-MySQL / MariaDB

-- צור את בסיס הנתונים (אם לא קיים)
CREATE DATABASE IF NOT EXISTS workout_manager
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

-- השתמש בבסיס הנתונים
USE workout_manager;

-- מחיקת טבלאות אם קיימות (לצורך בדיקות מאפס)
DROP TABLE IF EXISTS workout_exercises;
DROP TABLE IF EXISTS workouts;
DROP TABLE IF EXISTS exercises;
DROP TABLE IF EXISTS users;

-- טבלת משתמשים
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    join_date DATE NOT NULL DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB;

-- טבלת תרגילים
CREATE TABLE exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    muscle_group VARCHAR(50)
) ENGINE=InnoDB;

-- טבלת אימונים
CREATE TABLE workouts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_workouts_user
      FOREIGN KEY (user_id) REFERENCES users(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
) ENGINE=InnoDB;

-- טבלת חיבור בין אימון לתרגילים שבוצעו
CREATE TABLE workout_exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workout_id INT NOT NULL,
    exercise_id INT NOT NULL,
    sets INT NOT NULL CHECK (sets > 0),
    reps INT NOT NULL CHECK (reps > 0),
    weight DECIMAL(5,2) NOT NULL,
    CONSTRAINT fk_we_workout
      FOREIGN KEY (workout_id) REFERENCES workouts(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    CONSTRAINT fk_we_exercise
      FOREIGN KEY (exercise_id) REFERENCES exercises(id)
      ON DELETE RESTRICT
      ON UPDATE CASCADE
) ENGINE=InnoDB;
