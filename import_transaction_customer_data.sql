create database marketingdb;
GO
use marketingdb;
GO

-- technically you dont need these 2 tables, but just for reference
create table customer_data(
    customer_id int not null PRIMARY key,
    name NVARCHAR(255),
    email NVARCHAR(255),
    phone NVARCHAR(30),
    phone_ext NVARCHAR(10),
    address NVARCHAR(500),
    registration_date date,
    loyalty_status NVARCHAR(15)


);

create table transaction_data(
    transaction_id int not null primary key,
    customer_id int not null,
    amount decimal(20,2),
    transaction_date date, 
    product_category NVARCHAR(50),
    payment_method NVARCHAR(20),
    store_location NVARCHAR(100),
    promotion_tier NVARCHAR(30),
    constraint fk_transaction_customers foreign key (customer_id) REFERENCES customer_data(customer_id)

    
);

select * from transaction_data;


select * from orders;

select *
 from customer_data c 
left join orders o on c.customer_id = o.customer_id;



CREATE TABLE customer_master (
    CustomerID INT NOT NULL PRIMARY KEY,
    FirstName NVARCHAR(100) NULL,
    LastName  NVARCHAR(100) NULL,
    Email     NVARCHAR(255) NULL,
    Phone     NVARCHAR(30)  NULL,
    Address   NVARCHAR(500) NULL,

    CurrentFlag BIT NOT NULL DEFAULT 1,
    Version INT NOT NULL DEFAULT 1,

    LoyaltyTier NVARCHAR(50) NULL,
    PrevLoyaltyTier NVARCHAR(50) NULL,

    SubscriptionStart DATE NULL,
    SubscriptionEnd   DATE NULL
  );



  CREATE TABLE customer_update_stage (
  CustomerID INT NOT NULL,
  FirstName NVARCHAR(100) NULL,
  LastName  NVARCHAR(100) NULL,
  Email     NVARCHAR(255) NULL,
  Phone     NVARCHAR(30)  NULL,
  Address   NVARCHAR(500) NULL,
  LoyaltyTier NVARCHAR(50) NULL,
  SubscriptionStart DATE NULL,
  SubscriptionEnd   DATE NULL
);
