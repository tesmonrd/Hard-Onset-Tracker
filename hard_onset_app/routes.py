from flask import make_response, render_template, current_app, request
from .h_onset_model import db, User
from .audio_processor import LiveAudioSession, StreamAnalysis
import time


@current_app.route('/')
def index():
    return render_template('index.html', message=None, baseline=None)


@current_app.route('/baseline', methods=['GET'])
def handle_baseline():
    if request.method == 'GET':
        if User.query.filter(User.username == 'test').first():
            user = User.query.filter(User.username == 'test').first()
            user_baseline = user.baseline
        else:
            user_baseline = 0
    return render_template('baseline.html', user_baseline=user_baseline)


@current_app.route('/run_base', methods=['POST'])
def run_baseline():
    if request.method == 'POST':
        try:
            s = LiveAudioSession().clone()
            s.start_session()
            while time.time() < s.listen_time:
                s.listen()
            s.exit_session()
            stats = StreamAnalysis(s)
            stats.process_average_ftt()
            baseline = stats.baseline_fft
            message = "SUCCESS Baseline set to :{}".format(baseline)
        except Exception as e:
            message = "Error encountered: {}".format(e)
            baseline = None
        return render_template('index.html', message=message, baseline=baseline)


@current_app.route('/analyze')
def run_analysis():
    _bl = request.args.get('baseline')
    return render_template('analyzer.html', baseline=_bl)


@current_app.route('/execute_analysis')
def execute_analysis():
    _bl = request.args.get('baseline')
    _ttl = int(request.args.get('listen_time'))
    s = LiveAudioSession(_ttl, _bl, True).clone()
    stats = StreamAnalysis(s, _bl)
    s.start_session()
    while time.time() < s.listen_time:
        stats.listen_hard_onsets()
    graph = s.graph
    s.exit_session()
    return render_template('output.html', baseline=_bl, onset_count=stats.marked_h_onsets, graph=graph)


@current_app.route('/create_user/', methods=['GET'])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(
                f'{username} ({email}) already created!'
            )
        new_user = User(
            username=username,
            email=email,
            baseline=0
        )
        db.session.add(new_user)
        db.session.commit()
    return make_response(f"{new_user} successfully created!")