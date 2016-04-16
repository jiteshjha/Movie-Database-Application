import MySQLdb
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="remo161196", db="movieapp")
cursor = db.cursor()
MovieID = 4
cursor.execute("SELECT Review, ReviewDate, UserName FROM Review NATURAL JOIN User WHERE MovieID = %s ORDER BY ReviewID DESC",  (MovieID,))
data = cursor.fetchall()

print data
