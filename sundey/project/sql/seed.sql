-- seed.sql
-- הכנסת נתוני דוגמה לטבלאות מערכת Workout Manager
-- חשוב: להריץ אחרי schema.sql

USE workout_manager;

-- הכנסת משתמשים לדוגמה
INSERT INTO users (full_name, email, join_date) VALUES
  ('Daniel Levi',      'daniel@example.com',      '2025-01-10'),
  ('Noa Cohen',        'noa@example.com',         '2025-02-05'),
  ('Yossi Mizrahi',    'yossi@example.com',       '2025-03-12');

-- הכנסת תרגילים לדוגמה
INSERT INTO exercises (name, muscle_group) VALUES
  ('Bench Press',      'Chest'),
  ('Squat',            'Legs'),
  ('Deadlift',         'Back'),
  ('Overhead Press',   'Shoulders'),
  ('Pull Up',          'Back'),
  ('Bicep Curl',       'Arms');

-- הכנסת אימונים לדוגמה
-- נניח שהמשתמשים קיבלו מזהים 1,2,3 לפי סדר ה-INSERT
INSERT INTO workouts (user_id, date, notes) VALUES
  (1, '2025-04-01', 'Chest + triceps'),
  (1, '2025-04-03', 'Legs day'),
  (2, '2025-04-02', 'Back and biceps'),
  (3, '2025-04-05', 'Full body workout'),
  (2, '2025-04-06', 'Shoulders focus');

-- הכנסת תרגילים בתוך אימונים
-- נניח שהאימונים קיבלו מזהים 1..5 לפי הסדר
-- workout 1 – Chest + triceps (משתמש 1)
INSERT INTO workout_exercises (workout_id, exercise_id, sets, reps, weight) VALUES
  (1, 1, 4, 8, 80.00),   -- Bench Press
  (1, 6, 3, 12, 16.00);  -- Bicep Curl (כדוגמה לידיים)

-- workout 2 – Legs day (משתמש 1)
INSERT INTO workout_exercises (workout_id, exercise_id, sets, reps, weight) VALUES
  (2, 2, 5, 5, 100.00);  -- Squat

-- workout 3 – Back and biceps (משתמש 2)
INSERT INTO workout_exercises (workout_id, exercise_id, sets, reps, weight) VALUES
  (3, 3, 4, 6, 90.00),   -- Deadlift
  (3, 5, 3, 8, 0.00),    -- Pull Up – ללא משקל חיצוני
  (3, 6, 3, 10, 14.00);  -- Bicep Curl

-- workout 4 – Full body (משתמש 3)
INSERT INTO workout_exercises (workout_id, exercise_id, sets, reps, weight) VALUES
  (4, 2, 3, 8, 80.00),   -- Squat
  (4, 1, 3, 8, 70.00),   -- Bench Press
  (4, 3, 3, 6, 85.00);   -- Deadlift

-- workout 5 – Shoulders focus (משתמש 2)
INSERT INTO workout_exercises (workout_id, exercise_id, sets, reps, weight) VALUES
  (5, 4, 4, 10, 30.00);  -- Overhead Press
