
from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ssh...Big secret!'
#MySQL configurations

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'remo161196'
app.config['MYSQL_DATABASE_DB'] = 'movieapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# route to index.html
@app.route("/")
def main():
    return render_template('index.html')

# route to signup.html
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# interact with MySQL for sign up
@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/showAddMovie')
def showAddWish():
    return render_template('addMovie.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/addMovie',methods=['POST'])
def addMovie():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _releaseYear = request.form['inputReleaseYear']
            _rating = request.form['inputRating']
            _synopsis = request.form['inputSynopsis']
            _movieLength = request.form['inputMovieLength']
            _genre = request.form['inputGenre']
            _directorFirstName1 = request.form['inputDirectorFirstName1']
            _directorLastName1 = request.form['inputDirectorLastName1']
            _directorFirstName2 = request.form['inputDirectorFirstName2']
            _directorLastName2 = request.form['inputDirectorLastName2']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addMovie',(_title,_releaseYear,_rating,_synopsis,_movieLength,_genre))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')

            cursor.execute("SELECT MovieID FROM Movie WHERE Title = %s", (_title,))
            data = cursor.fetchone()
            MovieID = data[0]

            cursor.callproc('sp_addDirectorName',(_directorFirstName1,_directorLastName1))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                #return redirect('/userHome')
                cursor.execute("SELECT DirectorID FROM Director WHERE FirstName = %s AND LastName = %s", (_directorFirstName1,_directorLastName1,))
                data = cursor.fetchone()
                DirectorID = data[0]
                cursor.callproc('sp_addDirectedBy',(DirectorID,MovieID))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                else:
                    return render_template('error.html',error = 'An error occurred!')
            else:
                return render_template('error.html',error = 'An error occurred!')


            if _directorFirstName2 != '':
                cursor.callproc('sp_addDirectorName',(_directorFirstName2,_directorLastName2))
                data = cursor.fetchall()
                if len(data) is 0:
                    conn.commit()
                    #return redirect('/userHome')
                    cursor.execute("SELECT DirectorID FROM Director WHERE FirstName = %s AND LastName = %s", (_directorFirstName2,_directorLastName2,))
                    data = cursor.fetchone()
                    DirectorID = data[0]
                    cursor.callproc('sp_addDirectedBy',(DirectorID,MovieID))
                    data = cursor.fetchall()
                    if len(data) is 0:
                        conn.commit()
                        return redirect('/userHome')
                    else:
                        return render_template('error.html',error = 'An error occurred!')

                else:
                    return render_template('error.html',error = 'An error occurred!')



            #return render_template('error.html',error = str(MovieID))




        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()




if __name__ == "__main__":
    app.run()
