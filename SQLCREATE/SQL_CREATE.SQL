CREATE TABLE Passenger (
    SSN CHAR(9) PRIMARY KEY,
    first_Name VARCHAR(15),
    last_Name VARCHAR(15),
    Address VARCHAR(50),
    city VARCHAR(20),
    county VARCHAR(20),
    phone2 CHAR(10),
    bdate DATE
);
 
CREATE TABLE Train (
    Train_Number INT,
    Train_Name VARCHAR(100),
    Premium_Fare DECIMAL(10,2),
    General_Fare DECIMAL(10,2),
    Source_Station VARCHAR(100),
    Destination_Station VARCHAR(100),
    Weekdays TEXT,
    PRIMARY KEY (Train_Number, Train_Name)
);
 
CREATE TABLE Train_Status (
    TrainDate VARCHAR(9) NOT NULL,
    TrainName CHARVAR(100),
    Premium_Seats_Available INT,
    Gen_Seats_Available INT,
    Premium_Seats_Occupied INT,
    Gen_Seats_Occupied INT,
    PRIMARY KEY (TrainDate, TrainName),
    FOREIGN KEY (TrainName) REFERENCES Train(Train_Name)
);
 
CREATE TABLE Booking (
    Passenger_SSN CHAR(9),
    Train_Number INT,
    Ticket_Type TEXT CHECK(Ticket_Type IN('Premium', 'General')),
    Status TEXT CHECK(Status IN('Booked', 'WaitL')),
    PRIMARY KEY (Passenger_SSN, Train_Number),
    FOREIGN KEY (Passenger_SSN) REFERENCES Passenger(SSN),
    FOREIGN KEY (Train_Number) REFERENCES Train(Train_Number)
);