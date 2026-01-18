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



drop table transaction_data;

drop table customer_data;