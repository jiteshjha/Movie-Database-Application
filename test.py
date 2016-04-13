import MySQLdb
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="remo161196", db="movieapp")
cursor = db.cursor()
movie_name = "sdsd"
cursor.execute("SELECT * FROM Movie WHERE Title = %s", (movie_name,))
data = cursor.fetchone()
MovieID = data[0]

print
