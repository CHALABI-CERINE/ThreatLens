"""from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts')
def api_alerts():
    samples = [
        {"id": 1, "date": datetime.date.today().isoformat(), "source": "CVE", "severity":"High", "summary":"Sample vulnerability affecting xyz"},
        {"id": 2, "date": datetime.date.today().isoformat(), "source":"Blog", "severity":"Medium", "summary":"Emerging phishing campaign discussed in blog"}
    ]
    return jsonify(samples)

@app.route('/api/search')
def api_search():
    q = request.args.get('q','')
    # placeholder: return empty list
    return jsonify({"query": q, "results": []})

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=8501)
"""