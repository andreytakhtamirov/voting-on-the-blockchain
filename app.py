import requests
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# random md5 string
app.secret_key = '38a37cf643a419208265c7725ebf5bfb'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
@app.route('/getID')
def index():
    return render_template('index.html')


@app.route('/newVoter')
def new_voter():
    return render_template('newVoter.html')


@app.route('/addVoter', methods=['POST'])
def add_voter():
    if request.method == 'POST':
        name = request.form.get('fullName')
        date_of_birth = request.form.get('dateOfBirth')
        address = request.form.get('address')
        phone_number = request.form.get('phoneNumber')
        id = request.form.get('idNumber')

        headers = {'Content-Type': 'application/json'}
        api_url_mineblocks = 'http://localhost:3001/mineBlock'

        personal_details = 'VOTER' + '|' + name + '|' + date_of_birth + '|' + address + '|' + phone_number + '|' + id

        data = {'data': personal_details}

        response = requests.post(api_url_mineblocks, headers=headers, json=data)

        if response.status_code == 200:
            return redirect('/getID', code=301)
        else:
            return '<h2>Error adding Voter. Please try again</h2>' \
                   '<h3>Redirecting in 3 seconds...</h3> ' \
                   '<meta http-equiv="refresh" content="3;url=./addVoter" />'


@app.route('/verifyID', methods=['POST'])
def verify_id():
    if request.method == 'POST':
        name = request.form.get('fullName')
        date_of_birth = request.form.get('dateOfBirth')
        address = request.form.get('address')
        phone_number = request.form.get('phoneNumber')
        id = request.form.get('idNumber')
        personal_details = 'VOTER' + '|' + name + '|' + date_of_birth + '|' + address + '|' + phone_number + '|' + id

        api_url_getblocks = 'http://localhost:3001/blocks'
        headers = {'Content-Type': 'application/json'}

        response = requests.get(api_url_getblocks, headers=headers)
        block_dict = response.json()

        for element in block_dict:
            if element['data'] == personal_details:
                voter_hash = element['hash']
                session['voter_hash'] = voter_hash
                return redirect(url_for('show_candidates'))

        return '<h2>Error: User not found. You must register to vote.</h2>' \
               '<h3>Redirecting home in 3 seconds...</h3> ' \
               '<meta http-equiv="refresh" content="3;url=./" />'


@app.route('/candidates')
def show_candidates():
    return render_template('candidates.html')


@app.route('/castVote', methods=['POST'])
def cast_vote():
    if request.method == 'POST':
        if not session['voter_hash'] is None:
            candidate = request.form.get('candidate')

            voter_hash = session['voter_hash']
            headers = {'Content-Type': 'application/json'}
            api_url_mineblocks = 'http://localhost:3001/mineBlock'
            api_url_getblocks = 'http://localhost:3001/blocks'

            vote_data = 'VOTE' + '|' + candidate + '|' + voter_hash

            # destroy hash after after voting so we know they voted.
            session['voter_hash'] = None

            data = {'data': vote_data}

            # check if voted already
            response = requests.get(api_url_getblocks, headers=headers)
            block_dict = response.json()

            for element in block_dict:
                if element['data'] == vote_data:
                    # vote already present!
                    return '<h2>Error: your ballot was already cast. 1</h2>' \
                           '<h3>Redirecting home in 3 seconds...</h3> ' \
                           '<meta http-equiv="refresh" content="3;url=./" />'

            response = requests.post(api_url_mineblocks, headers=headers, json=data)

            if response.status_code == 200:
                return '<h2>Your ballot was cast! Thanks for voting.</h2>' \
                       '<h3>Redirecting home in 3 seconds...</h3> ' \
                       '<meta http-equiv="refresh" content="3;url=./" />'
            else:
                return '<h2>Error casting ballot. Please try again</h2>' \
                       '<h3>Redirecting home in 3 seconds...</h3> ' \
                       '<meta http-equiv="refresh" content="3;url=./" />'
        else:
            # catch attempt to vote twice with back button
            return '<h2>Error: your ballot was already cast.</h2>' \
                   '<h3>Redirecting home in 3 seconds...</h3> ' \
                   '<meta http-equiv="refresh" content="3;url=./" />'


@app.route('/ballots')
def display_ballots():
    headers = {'Content-Type': 'application/json'}
    api_url_getblocks = 'http://localhost:3001/blocks'

    response = requests.get(api_url_getblocks, headers=headers)
    block_dict = response.json()

    total_votes_to_display = '<h2>Votes</h2><ul>'

    for element in block_dict:
        if 'VOTE|' in element['data']:
            vote_data_elements = split_vote_data(element['data'])
            total_votes_to_display += '<li>Voter Hash: ' + vote_data_elements[2] + '<br>' \
                                      + ' Vote Hash: ' + element['hash'] + '<br>' \
                                      + 'Candidate: ' + vote_data_elements[1] + '<br><br></li>'

    total_votes_to_display += '</ul>'
    return total_votes_to_display


def split_vote_data(vote_data) -> list:
    data_elements = vote_data.split('|')
    return data_elements


@app.route('/voters')
def display_voters():
    headers = {'Content-Type': 'application/json'}
    api_url_getblocks = 'http://localhost:3001/blocks'

    response = requests.get(api_url_getblocks, headers=headers)
    block_dict = response.json()

    total_votes_to_display = '<h2>Registered Voters</h2>'
    voters = 0
    votes_cast = 0

    for element in block_dict:
        if 'VOTER|' in element['data']:
            voters += 1
            vote_data_elements = split_voter_data(element['data'])
            total_votes_to_display += 'Name: ' + vote_data_elements[1] + '<br>' \
                                      + ' Date of Birth: ' + vote_data_elements[2] + '<br>' \
                                      + 'Address: ' + vote_data_elements[3] + '<br>' \
                                      + 'Phone Number: ' + vote_data_elements[4] + '<br>' \
                                      + 'ID #: ' + vote_data_elements[5] + '<br>' \
                                      + 'Hash: ' + element['hash'] + '<br><br>'
        if 'VOTE|' in element['data']:
            votes_cast += 1

    total_votes_to_display += '<h3>Percent voted: ' + str(round(votes_cast/voters*100, 2)) + '%</h3>'

    return total_votes_to_display


def split_voter_data(voter_data) -> list:
    data_elements = voter_data.split('|')
    return data_elements


if __name__ == '__main__':
    app.run()
