from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///highscores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HighScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {'name': self.name, 'score': self.score}

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')    # Visualizar el archivo index.html

@app.route('/info')
def info():
    return render_template('info.html')

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
    app.run(debug=True)