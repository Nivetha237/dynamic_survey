from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_survey_data():
    with open('survey_data.json', 'r') as file:
        return json.load(file)

survey_data = load_survey_data()
responses = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    curr_id = request.form.get('curr_id', '1')  # Default to '1' if no current ID is provided

    if request.method == 'POST':
        reply = request.form.get('reply')
        sugg = request.form.get('sugg')

        if sugg:  # Handle suggestions
            responses[curr_id] = sugg
            print(f"Suggestion received: {sugg}")
            return redirect(url_for('thank_you'))

        if reply:
            responses[curr_id] = reply  # Update responses dictionary
            nxtquestion = nextque(reply, survey_data, curr_id)
            if nxtquestion:
                curr_id, _ = nxtquestion
                # Update curr_id for the next question
            else:
                return redirect(url_for('thank_you'))  # Redirect to thank you if no more questions

    quesdata = survey_data.get(curr_id, {})
    questext = quesdata.get('ques', 'No more questions.')
    options = quesdata.get('options', [])

    return render_template('survey.html', question=questext, options=options, curr_id=curr_id)

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

def nextque(reply, data, id):
    reply = reply.lower()  # Convert response to lowercase
    nxtquestion = data.get(id, {}).get('reply', {}).get(reply)
    if nxtquestion and nxtquestion in data:
        return nxtquestion, data[nxtquestion]['ques']
    return None

if __name__ == '__main__':
    app.run(debug=True)
