from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///highscores.db'       # Crear base de datos en path ./highscores.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HighScore(db.Model):
    # Crear tabla HighScore con columnas id, name y score
    id = db.Column(db.Integer, primary_key=True)    # Primary key: id único para cada registro
    name = db.Column(db.String(50), nullable=False) # nullable=False: No puede ser nulo
    score = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {'name': self.name, 'score': self.score}
    
    # def __repr__(self):
    #     return f'<HighScore {self.name} - {self.score}>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])    # Puede recibir peticiones POST y GET
def index():
    return render_template('index.html')    # Visualizar el archivo index.html

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    name = data.get('name')
    score = data.get('score')
    
    if name and score:
        new_score = HighScore(name=name, score=score)
        db.session.add(new_score)
        db.session.commit()

        # Keep only top 10 scores
        scores = HighScore.query.order_by(desc(HighScore.score)).all()
        if len(scores) > 10:
            for score_to_delete in scores[10:]:
                db.session.delete(score_to_delete)
            db.session.commit()

        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/get_high_scores')
def get_high_scores():
    high_scores = HighScore.query.order_by(desc(HighScore.score)).limit(10).all()
    return jsonify([score.to_dict() for score in high_scores])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)