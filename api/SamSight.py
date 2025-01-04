import pandas as pd
df=pd.read_csv(r"C:\Users\Rohit\Projects\walmart\sight\api\data.csv")
df["Date"]=pd.to_datetime(df["Date"])
df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
print(df.info())


import psycopg2
connection = psycopg2.connect(
        host="localhost",
        database="sight",
        user="postgres",
        password="210282",
        port=5432
    )
    
    # Creating a cursor object to interact with the database
cur = connection.cursor()




cur.execute('''CREATE TABLE STORE(
    Invoice_ID VARCHAR(20) PRIMARY KEY,
    Branch VARCHAR(1),
    City VARCHAR(30),
    Customer_Type VARCHAR(10),
    Gender VARCHAR(7),
    Product_Type VARCHAR(30),
    Price FLOAT,
    Quantity INT,
    Tax FLOAT,
    Total FLOAT,
    Date DATE,
    Time TIME,
    Payment VARCHAR(20),
    Cogs FLOAT,
    Gross_mp FLOAT,
    Gross_inc FLOAT,
    Rating FLOAT
    )''')



for i in range(1000):
    val=tuple(df.iloc[i].values)
    cur.execute("INSERT INTO STORE VALUES "+ str(val))
    



connection.commit()
connection.close()