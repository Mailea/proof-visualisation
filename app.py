"""The application entry point"""

import os

from flask import Flask, render_template, request, session
from flask_session import Session

from proof_visualization.controller import controller
from proof_visualization.model.search import find_common_consequences

VIEW_DIR = os.path.join(os.path.dirname(__file__), 'proof_visualization', 'view')
TEMPLATE_DIR = os.path.join(VIEW_DIR, 'templates')
STATIC_DIR = os.path.join(VIEW_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
SESSION_TYPE = 'filesystem'
SESSION_FILE_THRESHOLD = 1
app.config.from_object(__name__)
Session(app)


@app.route("/", methods=['GET'])
def home():
    controller.init_controller()
    return render_template('main.html',
                           dagData=controller.get_layout(), historyLength=session['dags'][0].number_of_history_steps(),
                           reset=True,
                           legend=controller.get_legend(), preSelection=[], isInitial=True)


@app.route("/", methods=['POST'])
def handle_post_request():
    params = request.form.to_dict()
    reset = False
    selection = []
    initial = False
    if params.get('file'):
        reset = True
        controller.init_dag(params['file'])
        refresh_history_state()
        initial = True
    elif params.get('selection'):
        selection = [int(param) for param in params['selection'].split(',')]
        reset = True

        if params.get('up'):
            controller.filter_non_parents(selection)
        else:
            controller.filter_non_consequences(selection)
        refresh_history_state()
    elif params.get('reset'):
        reset = True
        controller.reset_dag()
        refresh_history_state()
        selection = params.get('selection', [])
        initial = len(session['dags']) == 1
    elif params.get('consequences'):
        node_ids = {int(id_) for id_ in params['consequences'].split(',')}
        selection = find_common_consequences(session['dags'][-1], node_ids)
    else:
        update_history_state(params)
    return render_template('main.html',
                           dagData=controller.get_layout(), historyState=session['history_state'],
                           historyLength=session['dags'][0].number_of_history_steps(), reset=reset,
                           legend=controller.get_legend(), preSelection=selection, isInitial=initial)


@app.before_first_request
def clear_session():
    session.clear()


def update_history_state(request_params):
    # update history state to new canidate value
    if request_params.get('increase'):
        history_state = session['history_state'] + 1
    elif request_params.get('decrease'):
        history_state = session['history_state'] - 1
    elif request_params.get('slide'):
        history_state = int(request_params['slide'])

    # make sure candidate is in meaningful interval and change if necessary
    history_state = max(0, history_state)

    last_step = session['dags'][0].last_step()
    history_state = min(history_state, last_step)

    session['history_state'] = history_state


def refresh_history_state():
    session['history_state'] = session['dags'][0].last_step()


if __name__ == '__main__':
    app.run()
