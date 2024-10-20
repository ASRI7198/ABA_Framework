from flask import Flask, render_template, request, redirect, url_for, session
import re
import Argument
import ABA
import Assumption
import Attack
import Literal
import Rule
from Preferences import Preferences
from ReverseAttack import generate_normal_reverse_attacks

app = Flask(__name__, template_folder='template')
import secrets

# Génère une clé secrète de 16 bytes en base64
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


def validate_input(input_text):
    import re

    pattern = r'''
    L:\s*\[(?P<L>(?:\w+(?:,\s*)?)+)\]\s*      # L: [a,b,c,q,p,r,s,t]
    A:\s*\[(?P<A>(?:\w+(?:,\s*)?)+)\]\s*      # A: [a,b,c]
    C\((?P<C1>\w+)\):\s*(?P<value1>\w+)\s*    # C(a): r
    C\((?P<C2>\w+)\):\s*(?P<value2>\w+)\s*    # C(b): s
    C\((?P<C3>\w+)\):\s*(?P<value3>\w+)\s*    # C(c): t
    (?P<rules>(?:\[\w+\]:\s*\w+\s*<-?\s*(?:\w+(?:,\s*)?)*\s*)+)  # [r1]: p <- q,a
    PREF:\s*(?P<PREF>\w+)\s*>\s*(?P<other>\w+)  # PREF: a > b
    '''
    input_text = re.sub(r'\s+', '', input_text)
    match = re.match(pattern, input_text, re.VERBOSE)

    # Débogage : afficher l'entrée et le match

    return match is not None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['text_input']

        if validate_input(input_text):
            # Redirection vers une autre route (exemple : options) avec l'entrée utilisateur
            return redirect(url_for('options', user_input=input_text))
        else:
            error_message = "L'entrée ne respecte pas le format requis."
            return render_template('Home.html', error=error_message)

    return render_template('Home.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['text_input']
        return redirect(url_for('options', user_input=user_input))

    return render_template('Home.html')


@app.route('/options/<user_input>', methods=['GET', 'POST'])
def options(user_input):
    Ltexte, Atexte, Ctexte, R, PREF = parse_input(user_input)
    L = []
    A2 = []
    for item in Ltexte:
        e = f'"{item}"'
        literal = Literal.Literal(e)
        L.append(literal)

    keys = list(Ctexte.keys())  # Liste des clés
    value = list(Ctexte.values())
    con = []
    result = []
    for i, j in zip(keys, value):
        e = f"{i}"
        f = f"{j}"
        literal1 = Literal.Literal(e)
        literal2 = Literal.Literal(f)
        con.append(literal1)
        result.append(literal2)

    A = Assumption.Assumption('A', con, result)
    # print(A.display())
    keysR = list(R.keys())  # Liste des clés
    valueR = list(R.values())

    list_conclusion = []
    list_premisse = []
    for item in valueR:
        # Séparer chaque élément en utilisant '<-'
        key_value = item.split(' <- ')
        list_conclusion.append(key_value[0].strip())  # Clé
        list_premisse.append(key_value[1].strip())  # Valeur

    conclusion = []
    regle = []
    for i, j in zip(list_conclusion, keysR):
        e = f"{i}"
        # f = f"{j}"
        literal1 = Literal.Literal(e)
        # literal2 = Literal.Literal(f)
        conclusion.append(literal1)
        regle.append(j)
    listePremisse = []
    for item in list_premisse:
        if len(item) == 0 or len(item) == 1:
            e = f"{item}"
            literal = Literal.Literal(e)
            listePremisse.append(literal)
        else:
            w = []
            for i in item:
                if i != ",":
                    i = i.strip(" ")
                    e = f"{i}"
                    literal = Literal.Literal(e)
                    w.append(literal)
            listePremisse.append(w)
    R = []
    for i, j, k in zip(regle, listePremisse, conclusion):
        rule = Rule.Rule(i, j, k)
        # print(rule.display())
        R.append(rule)

    Ga = Argument.Argument.generate_arguments(R, A)

    #
    def remove_duplicates(lst):
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create_arguments':
            Ga = Argument.Argument.generate_arguments(R, A)
            result = Argument.Argument.print_arguments(Ga)
            result = [arg.display() for arg in result]
            session['result'] = result

        elif action == 'create_attacks':
            result = Attack.generate_attacks(Ga, A)
            result = [arg.display() for arg in result]
            session['result'] = result
        elif action == 'auto_convert_non_circular':
            aba = ABA.ABA(L, R, A)
            aba.circularToNonCircular()
            NewR1 = []
            NewL1 = []
            # #print("NewR : ",NewR)
            for i in R:
                # print("type(i) : ",type(i))
                # if isinstance(i, list) :
                #     for j in i :
                #         print("Ruel Rida2 : ", j.display())
                #         NewR1.append(j.display())
                # else:
                #     print("Ruel Rida : ", i.display())
                    NewR1.append(i.display())

            for i in L:
                # if isinstance(i, list):
                #     for j in i:
                #         NewL1.append(j.display())
                # else:
                    NewL1.append(i.display())
            liste3=[]
            liste3.append("3")
            result = [NewL1,NewR1,liste3]

            session['result'] = result
        elif action == 'auto_convert_atomic':
            aba = ABA.ABA(L, R, A)
            liste1, liste2, liste3 = aba.toAtomic()
            liste4 = []
            liste4.append("4")
            result = [liste1, liste2, liste3,liste4]
            session['result'] = result
        elif action == 'handle_preferences_assumptions':
            PREF = PREF.split('>')
            a = Literal.Literal(PREF[0].strip())
            b = Literal.Literal(PREF[1].strip())
            pref = Preferences([a], [b])
            result = pref.display()
            result = [result]
            session['result'] = result
        elif action == 'handle_normal_reverse_attacks':
            PREF = PREF.split('>')
            a = Literal.Literal(PREF[0].strip())
            b = Literal.Literal(PREF[1].strip())
            pref = Preferences([a], [b])
            normal, reverse = generate_normal_reverse_attacks(A, pref, R)
            print("Normal Attacks")
            lisenormal = [i.display() for i in normal]
            lisereverse = [i.display() for i in reverse]
            lisenormal = remove_duplicates(lisenormal)
            lisereverse = remove_duplicates(lisereverse)
            for att in lisenormal:
                print(att)

            print("Reverse Attacks")

            for att in lisereverse:
                print(att)
            result = [lisenormal, lisereverse]
            session['result'] = result

        return redirect(url_for('result'))

    return render_template("Options.html")


@app.route('/result')
def result():
    result = session.get('result', [])
    print(result)
    return render_template('Result.html', result=result)
    # result = request.args.get('result')  # Récupère le paramètre 'result' de l'URL
    # return render_template("Result.html", result=result)


def parse_input(text):
    L, A, C, R, PREF = [], [], {}, {}, ""
    lines = text.splitlines()
    for line in lines:
        if line.startswith("L:"):
            L = re.findall(r'\w+', line[2:])
        elif line.startswith("A:"):
            A = re.findall(r'\w+', line[2:])
        elif line.startswith("C("):
            key = re.search(r'C\((\w)\)', line).group(1)
            value = re.search(r': (\w+)', line).group(1)
            C[key] = value
        elif line.startswith("[r"):
            rule_key = re.search(r'r(\d+)', line).group(0)
            rule_value = re.search(r': (.+)', line).group(1)
            R[rule_key] = rule_value
        elif line.startswith("PREF:"):
            PREF = re.search(r'PREF: (.+)', line).group(1)

    return L, A, C, R, PREF


if __name__ == '__main__':
    app.run(debug=True)
