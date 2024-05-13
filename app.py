from flask import Flask, url_for, render_template, g, request
import sqlite3

app = Flask(__name__)

def createdatabase():

    sql="""CREATE TABLE IF NOT EXISTS `Skladnik` (
        `ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
        `Nazwa` VARCHAR(45) NULL,
        `kalorie_na_100gr` INTEGER  NULL,
        `Dodatkowe` VARCHAR(45) NULL
        );

            """
    g.sqlite_db.execute(sql)
    sql="""

        CREATE TABLE IF NOT EXISTS `Administrator` (
        `nazwa_identyfikacyjna` VARCHAR(30) NOT NULL,
        `Mail` VARCHAR(60) NOT NULL,
        `Hasło` VARCHAR(65) NOT NULL,
        PRIMARY KEY (`nazwa_identyfikacyjna`),
        UNIQUE  (`Mail` ASC));

            """
    g.sqlite_db.execute(sql)
    sql="""   

        CREATE TABLE IF NOT EXISTS `Posiłek` (
        `ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
        `Administrator_nazwa_identyfikacyjna` VARCHAR(30) NOT NULL,
        `Nazwa` VARCHAR(45) NOT NULL,
        UNIQUE ( `Administrator_nazwa_identyfikacyjna`),
        CONSTRAINT `fk_Posiłek_Administrator1`
            FOREIGN KEY (`Administrator_nazwa_identyfikacyjna`)
            REFERENCES `Administrator` (`nazwa_identyfikacyjna`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION);


            """
    g.sqlite_db.execute(sql)
    sql="""
        CREATE TABLE IF NOT EXISTS `posrednia_skladnik_posilek` (
        `ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
        `Posiłek_ID` INT NOT NULL,
        `Skladnik_ID` INT NOT NULL,
        `Ilosc` FLOAT NOT NULL,
        CONSTRAINT `fk_posrednia_skladnik_posilek_Posiłek1`
            FOREIGN KEY (`Posiłek_ID`)
            REFERENCES `Posiłek` (`ID`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_posrednia_skladnik_posilek_Skladnik1`
            FOREIGN KEY (`Skladnik_ID`)
            REFERENCES `Skladnik` (`ID`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION);
            """
    g.sqlite_db.execute(sql)
    g.sqlite_db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect('data5.db3')
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
        createdatabase()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#def return_units(id):
#    db=get_db()
#    sql="select ilosc ,Jednostka_Jednostka from posrednia_skladnik_jednostka where Skladnik_ID=?;"
#    cursor=db.execute(sql,[id])
#    info=cursor.fetchall()
#    return info


class Posilek:
    def __init__(self, name, calories, ingredients):
        self.name = name
        self.calories = calories
        self.ingredients = ingredients


@app.route('/')
def index():

    a1 = Posilek("Zupa",20000,['Marchew', 'Kości', 'Kostka rosołowa'])
    a2 = Posilek("Zupa",20000,['Twaróg', 'Kości', 'Kostka rosołowa'])
    info = [a1,a1,a1,a2,a2,a1,a2,a1,a2]
    return render_template('Wyswietlenie.html', info=info)


@app.route('/skl')
def skladniki():

    db = get_db()
    sql = "select * from Skladnik;"
    cursor = db.execute(sql)
    info = cursor.fetchall()
    return render_template('wyswietl_skl.html',info=info)


@app.route('/wpr_po', methods=['GET','POST'])
def wpr():
    if(request.method == 'POST'):
        return render_template('base.html')
    else:
        db=get_db()
        sql= "select * from Skladnik;"
        cursor=db.execute(sql)

        return render_template('wprowadz_posilek.html',ingredients=cursor.fetchall())

@app.route('/wpr_skl', methods=['GET','POST'])
def wpr_skl():

    db= get_db()
    if request.method == 'POST':

        sql = 'insert into Skladnik values (null, ?, ? ,?);'
        nazwa=request.form['nazwa']
        kalorie=request.form['kalorie']
        db.execute(sql,[nazwa, kalorie, ''])
        db.commit()
        return render_template('wprowadz_skl.html',info='Dane zostały wprowadzone poprawnie')
    else:
        return render_template('wprowadz_skl.html',info='')



if __name__=='__main__':
    app.run(port=8031,debug=True)










