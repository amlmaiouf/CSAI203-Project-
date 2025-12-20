IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'elderly_care_system')
BEGIN
    CREATE DATABASE elderly_care_system;
END
GO

USE elderly_care_system;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'User')
BEGIN
    CREATE TABLE [User] (
        user_id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        email NVARCHAR(100) UNIQUE NOT NULL,
        password NVARCHAR(255) NOT NULL,
        role NVARCHAR(50) DEFAULT 'Elderly' CHECK (role IN ('Admin', 'Elderly', 'Staff', 'Doctor', 'Caregiver')),
        phone_number NVARCHAR(20),
        address NVARCHAR(255),
        profile NVARCHAR(MAX),
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE()
    );

    CREATE INDEX IX_User_Email ON [User](email);
    CREATE INDEX IX_User_Role ON [User](role);
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Service')
BEGIN
    CREATE TABLE [Service] (
        service_id INT IDENTITY(1,1) PRIMARY KEY,
        service_name NVARCHAR(100) NOT NULL,
        type NVARCHAR(50) NOT NULL CHECK (type IN ('Medical', 'Housekeeping', 'Grocery', 'Pharmacy', 'Pet Care', 'Car Cleaning', 'Nursing', 'Delivery', 'Companionship')),
        price DECIMAL(10,2) NOT NULL DEFAULT 0,
        description NVARCHAR(MAX),
        is_available BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE()
    );

    CREATE INDEX IX_Service_Type ON [Service](type);
    CREATE INDEX IX_Service_Available ON [Service](is_available);
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Order')
BEGIN
    CREATE TABLE [Order] (
        order_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        order_date DATETIME DEFAULT GETDATE(),
        status NVARCHAR(50) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Confirmed', 'In Progress', 'Completed', 'Cancelled')),
        total_amount DECIMAL(10,2) DEFAULT 0,
        payment_status NVARCHAR(50) DEFAULT 'Unpaid' CHECK (payment_status IN ('Unpaid', 'Paid', 'Refunded')),
        notes NVARCHAR(MAX),
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (user_id) REFERENCES [User](user_id) ON DELETE CASCADE
    );

    CREATE INDEX IX_Order_User ON [Order](user_id);
    CREATE INDEX IX_Order_Status ON [Order](status);
    CREATE INDEX IX_Order_Date ON [Order](order_date);
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Order_Service')
BEGIN
    CREATE TABLE [Order_Service] (
        order_service_id INT IDENTITY(1,1) PRIMARY KEY,
        order_id INT NOT NULL,
        service_id INT NOT NULL,
        quantity INT DEFAULT 1,
        price DECIMAL(10,2) NOT NULL,
        scheduled_date DATE,
        scheduled_time TIME,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (order_id) REFERENCES [Order](order_id) ON DELETE CASCADE,
        FOREIGN KEY (service_id) REFERENCES [Service](service_id) ON DELETE CASCADE
    );

    CREATE INDEX IX_OrderService_Order ON [Order_Service](order_id);
    CREATE INDEX IX_OrderService_Service ON [Order_Service](service_id);
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Feedback')
BEGIN
    CREATE TABLE [Feedback] (
        feedback_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        service_id INT NOT NULL,
        order_id INT,
        date DATE DEFAULT CAST(GETDATE() AS DATE),
        rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
        comment NVARCHAR(MAX),
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (user_id) REFERENCES [User](user_id) ON DELETE CASCADE,
        FOREIGN KEY (service_id) REFERENCES [Service](service_id) ON DELETE CASCADE,
        FOREIGN KEY (order_id) REFERENCES [Order](order_id) ON DELETE NO ACTION
    );

    CREATE INDEX IX_Feedback_User ON [Feedback](user_id);
    CREATE INDEX IX_Feedback_Service ON [Feedback](service_id);
    CREATE INDEX IX_Feedback_Rating ON [Feedback](rating);
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Notification')
BEGIN
    CREATE TABLE [Notification] (
        notification_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        title NVARCHAR(100) NOT NULL,
        message NVARCHAR(MAX),
        type NVARCHAR(50) CHECK (type IN ('Order', 'Appointment', 'Payment', 'System', 'Reminder')),
        is_read BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (user_id) REFERENCES [User](user_id) ON DELETE CASCADE
    );

    CREATE INDEX IX_Notification_User ON [Notification](user_id);
    CREATE INDEX IX_Notification_Read ON [Notification](is_read);
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Service_History')
BEGIN
    CREATE TABLE [Service_History] (
        history_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        service_id INT NOT NULL,
        order_id INT,
        request_date DATETIME DEFAULT GETDATE(),
        completion_date DATETIME,
        status NVARCHAR(50) DEFAULT 'Requested' CHECK (status IN ('Requested', 'In Progress', 'Completed', 'Cancelled')),
        notes NVARCHAR(MAX),
        created_at DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (user_id) REFERENCES [User](user_id) ON DELETE CASCADE,
        FOREIGN KEY (service_id) REFERENCES [Service](service_id) ON DELETE CASCADE
    );

    CREATE INDEX IX_ServiceHistory_User ON [Service_History](user_id);
    CREATE INDEX IX_ServiceHistory_Service ON [Service_History](service_id);
END
GO

PRINT 'Database schema created successfully!';
GO
