"""from flask import Flask, render_template, request, jsonify
from .db import init_db, SessionLocal
from .models import Alert
from .collectors_nvd import fetch_nvd, store_alerts
from .scheduler import start_scheduler
from sqlalchemy import desc
import math

app = Flask(__name__, template_folder='templates', static_folder='static')

# initialize DB & scheduler
init_db()
try:
    start_scheduler()
except Exception as e:
    print('Scheduler could not be started at boot:', e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts')
def api_alerts():
    page = int(request.args.get('page', 1))
    per = int(request.args.get('per', 20))
    q = request.args.get('q')
    db = SessionLocal()
    try:
        query = db.query(Alert).order_by(desc(Alert.published_date))
        if q:
            query = query.filter(Alert.summary.ilike(f"%{q}%"))
        total = query.count()
        items = query.offset((page-1)*per).limit(per).all()
        return jsonify({
            'page': page,
            'per': per,
            'total': total,
            'pages': math.ceil(total/per) if per else 1,
            'items': [i.to_dict() for i in items]
        })
    finally:
        db.close()

@app.route('/api/fetch-now', methods=['POST'])
def api_fetch_now():
    # simple trigger to run a fetch synchronously (could be protected later)
    items = fetch_nvd(max_results=100)
    added = store_alerts(items)
    return jsonify({'fetched': len(items), 'added': added})

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=8501)
"""