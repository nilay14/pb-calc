from flask import Flask,render_template,jsonify,session,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField,RadioField,TextField
import os
from cric import playing
from cricbs import calculate
from flask_session import Session

app=Flask(__name__)

app.secret_key='pHrVilFLJX2YnBMuVwjUULfzCZWPeLij'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:P0A3kl8yfTqhGzZVjkFm@database-1.c4w8u3yld3az.ap-south-1.rds.amazonaws.com/master'
db = SQLAlchemy(app)



class Match(db.Model):
    __tablename__='match_list'
    id = db.Column('id',db.Integer,primary_key=True)
    date = db.Column('date',db.Unicode)
    series_name=db.Column('series_name',db.Unicode)
    match_name=db.Column('match_name',db.Unicode)
    match_link=db.Column('match_link',db.Unicode)

class Myform(FlaskForm):
    x=db.session.query(Match.date).distinct().all()
    t=[]
    m=[]
    n=[]
    for ex in x:
        id_var=db.session.query(Match.id,Match.date).filter_by(date=ex).first()
        t.append((id_var[0],id_var[1]))
    series_name=db.session.query(Match.series_name,Match.date).filter_by(date=x[0]).distinct().all()
    ser_first=series_name[0]
    for each in series_name:
        temp=db.session.query(Match.id,Match.date,Match.series_name).filter_by(date=each[1]).filter_by(series_name=each[0]).first()[0]
        m.append((temp,each[0]))
    match_name=db.session.query(Match.id,Match.date,Match.series_name,Match.match_name).filter_by(date=x[0]).filter_by(series_name=ser_first[0]).all()
    for each in match_name:
        n.append((each[0],each[3]))
    date=SelectField('Date',choices=t)
    match_series=SelectField('Series Name',choices=m)
    match_name=SelectField('Match Name',choices=n)
    submit=SubmitField("Submit")

class Playin_xi(FlaskForm):
    team1=TextField(_name='playerdata')
    team2=TextField(_name='playerdata')
    submit=SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form = Myform()
    if request.method=="POST":
        id_match=form.match_name.data
        mat_link=db.session.query(Match.id,Match.match_link).filter_by(id=id_match).first()[1]
        session['link']=mat_link
        return redirect(url_for('sel_players'))   
    return render_template('select.html',form=form)

@app.route('/player/team',methods=['GET','POST'])
def sel_players():
    form = Playin_xi()
    mat_link=session['link']
    #teams=playing(mat_link)
    team=1
    if request.method=='POST':
        return redirect(url_for('team'))
    return render_template('select_players.html',form=form,team=team)




@app.route('/date/<date_index>',methods=['GET','POST'])
def ser(date_index):
    date=db.session.query(Match.id,Match.date).filter_by(id=int(date_index)).first()[1]
    allser=db.session.query(Match.date,Match.series_name).filter_by(date=date).distinct().all()

    serArr=[]
    for each_series in allser:
        serObj={}
        serObj['id']=db.session.query(Match.id,Match.date,Match.series_name).filter_by(date=each_series[0]).filter_by(series_name=each_series[1]).first()[0]
        #serObj['id']=each_series[0]
        serObj['series_name']=each_series[1]
        serArr.append(serObj)
    session['series']=serArr
    return jsonify({'series':serArr})

@app.route('/name/<series_name>')
def mat(series_name):
    ser_name=db.session.query(Match.id,Match.series_name,Match.date).filter_by(id=series_name).first()
    match_list=db.session.query(Match.date,Match.series_name,Match.match_name).filter_by(date=ser_name[2]).filter_by(series_name=ser_name[1]).all()
    matArr=[]
    for each_match in match_list:
        matd={}
        matd['id']=db.session.query(Match.id,Match.date,Match.match_name).filter_by(date=each_match[0]).filter_by(match_name=each_match[2]).first()[0]
        matd['match_name']=each_match[2]
        matArr.append(matd)
    
    return jsonify({'matches':matArr})

@app.route('/players/list')
def playerslist():
    suggestions=[]
    query = request.args.get('query')
    print(query)
    mat_link=session['link']
    players_list=playing(mat_link)
    print(players_list)
    for each in players_list:
        try:
            if each['value'].lower().startswith(query.lower()) or each['value'].lower().split()[1].startswith(query.lower())  :
                suggestions.append({
                    'data':each['value'],
                    'value':each['value'],
                })
        except IndexError:
            if each['value'].lower().startswith(query):
                suggestions.append({
                    'data':each['value'],
                    'value':each['value'],
                })
    return jsonify({'suggestions':suggestions})
@app.route('/players/calculate',methods=['POST'])

def team():
    team1=request.form.getlist('team1')
    print(team1)
    team2=request.form.getlist('team2')
    mat_link=session['link']
    print("session"+mat_link)
    runs=calculate(mat_link,team1,team2)
    return render_template('final_runs.html',calc=runs)
    
if __name__ == "__main__":
    app.run(debug=True)