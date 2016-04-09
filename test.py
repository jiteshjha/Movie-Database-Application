import MySQLdb
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="remo161196", db="movieapp")
cursor = db.cursor()
movie_name = "sdsd"
cursor.execute("SELECT * FROM Movie WHERE Title = %s", (movie_name,))
data = cursor.fetchone()
data_dict = []
data_dic = {
        'MovieID': data[0],
        'Title': data[1],
        'ReleaseYear': data[2],
        'Rating': data[3],
        'Synopsis': data[4],
        'MovieLength': data[5],
        'GenreName': data[6]}
print data_dic
