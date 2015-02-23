import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(database="vivek")
cur = conn.cursor()

query1 = """
SELECT date, close_price
FROM stocks WHERE stock_name = 'TSLA'
AND date > '01/01/2000'
ORDER BY date
"""

query2 = """
SELECT date, close_price
FROM stocks WHERE stock_name = 'NFLX'
AND date > '01/01/2000'
ORDER BY date
"""

query3 = """
SELECT date, close_price
FROM stocks WHERE stock_name = 'MSFT'
AND date > '01/01/2000'
ORDER BY date
"""
query4 = """
SELECT date, close_price
FROM stocks WHERE stock_name = 'BA'
AND date > '01/01/2000'
ORDER BY date
"""

query5 = """
SELECT date, close_price
FROM stocks WHERE stock_name = 'XOM'
AND date > '01/01/2000'
ORDER BY date
"""

cur.execute(query1)
tsla_data = cur.fetchall()

cur.execute(query2)
nflx_data = cur.fetchall()

cur.execute(query3)
msft_data = cur.fetchall()

cur.execute(query4)
ba_data = cur.fetchall()

cur.execute(query5)
xom_data = cur.fetchall()

cur.close()
conn.close()

#print msft_data[:2]
#print msft_data[-2:]
#print zip(*msft_data)


date1, close_price1 = zip(*tsla_data)
date2, close_price2 = zip(*nflx_data)
date3, close_price3 = zip(*msft_data)
date4, close_price4 = zip(*ba_data)
date5, close_price5 = zip(*xom_data)



#Tesla plot
#plt.plot(date1, close_price1, label='Tesla')
#Netflix plot
#plt.plot(date2, close_price2, label='Netflix')
#Microsoft plot
#plt.plot(date3, close_price3, label='Microsoft')
#Boeing plot
plt.plot(date4, close_price4, label='Boeing')
plt.plot(date5, close_price5, label='Exxon')

plt.legend(loc='upper left')
plt.xlabel("Time")
plt.ylabel("Closing Price")
plt.show()
