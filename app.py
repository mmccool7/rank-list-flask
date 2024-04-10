from flask import Flask, render_template, request, session, url_for, redirect, render_template_string
from flask_session import Session

app = Flask(__name__)

SECRET_KEY = '76d0b7b4ef979d2b9f423ef7908b3f67ed344c5d23685c61'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ranklist', methods=['GET', 'POST'])
def rank():
    return render_template('ranklist.html')

@app.route('/programlog', methods=['GET', 'POST'])
def logprograms():
    session['sorted_sums'] = {}
    session['sums'] = {}
    session['dict1'] = {}
    programlist = []
    session['programs'] = []
    if request.method == 'POST':
        programs = request.form.getlist('text')
        for program in programs:
            programlist.append(program)
        session['programs'] = programlist
        program_count = len(programlist)
        num_program_list = []
        for i in range(1,program_count+1):
            num_program_list.append(i)
        session['num_program_list'] = num_program_list
        programs_int_list = len(num_program_list)
        session['num_programs'] = programs_int_list
    return redirect(url_for('attributes'))

@app.route('/attributes', methods=['GET', 'POST'])
def attributes():
    return render_template('attributes.html')

@app.route('/attributeslog', methods=['GET', 'POST'])
def logattributes():
    attributelist = []
    session['attributes'] = []
    if request.method == 'POST':
        attributes = request.form.getlist('text')
        for attribute in attributes:
            attributelist.append(attribute)
        session['attributes'] = attributelist
    return redirect(url_for('list_attributes'))

@app.route('/attributeslist')
def list_attributes():
    attributes = session['attributes']
    return render_template('attr_list.html', attributes = attributes)

@app.route('/attributes/<attr>', methods = ['GET', 'POST'])
def show_attribute(attr):
    session.pop('attr', None)
    if attr in session['attributes']:
        session['attr'] = attr
        return render_template('show_attr.html', attr=attr, programs = session['programs'], prog_list = session['num_program_list'])
    else:
        return "Attribute not found", 404
    
@app.route('/submissionlog', methods=['GET', 'POST'])
def logsubmission():
    if request.method == 'POST':
        attr = session['attr']
        key = attr
        dict1 = session['dict1']
        score = request.form.getlist('select')
        numbers_int_list = [int(number_str) for number_str in score]
        index = 0
        dict1.update({key : numbers_int_list})
        session['dict1'] = dict1
    return redirect(url_for('list_attributes'))

@app.route('/finalcalculations', methods=['GET', 'POST'])
def finalcalculations():
    my_dict = {}
    attributes = session['dict1']
    programs = session['programs']
    num_attributes = len(attributes)
    for attr, score in attributes.items():
        new_list = []
        for i in score:
            new_list.append(i * num_attributes)
        num_attributes -= 1
        my_dict[attr] = new_list

    named_lists = {name: [] for name in programs}

    for index, values in enumerate(zip(*my_dict.values())):
        if index < len(programs):  # Check to ensure there's a corresponding name
            named_lists[programs[index]] = list(values)
    
    sums = {}

    for name, numbers in named_lists.items():
        sums[name] = sum(numbers)

    sorted_sums = sorted(sums.items(), key=lambda item: item[1], reverse=True)
    session['sorted_sums'] = sorted_sums
    session['sums'] = sums
    return redirect(url_for('showscores'))

@app.route('/scores', methods=['GET', 'POST'])
def showscores():
    possible = 0
    x = session['num_programs']
    for i in range(x):
        possible += (x * (i+1))
    return render_template('show_scores.html', sorted_sums = session['sorted_sums'], sums = session['sums'], programs = session['num_programs'], possible = possible)

@app.route('/done', methods=['GET', 'POST'])
def done():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)