CREATE TABLE IF NOT EXISTS UserThresholds (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    RFID TEXT NOT NULL,
    Name TEXT NOT NULL,
    TempThreshold INTEGER,
    HumidityThreshold INTEGER,
    LightIntensityThreshold INTEGER
);

-- Insert sample data
INSERT INTO UserThresholds (RFID, Name, TempThreshold, HumidityThreshold, LightIntensityThreshold)
VALUES ('RFID123', 'Maximus Taube', 25, 60, 400),
       ('RFID123', 'Arsh', 24, 65, 450),
       ('RFID123', 'Seb', 23, 70, 500),
       ('RFID123', 'Trevor', 40, 100, 600),
       ('RFID123', 'Sakku', 18, 50, 250),
       ('RFID123', 'Eve Wilson', 22, 75, 480),
       ('RFID123', 'Sarah Lee', 27, 50, 410),
       ('RFID123', 'Mike Anderson', 21, 68, 490),
       ('RFID123', 'Emily Taylor', 28, 45, 430),
       ('RFID123', 'David Clark', 20, 80, 550),
       ('RFID123', 'Linda Martinez', 29, 40, 460);
