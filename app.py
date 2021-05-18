from flask import Flask, render_template, request

app = Flask(__name__)


def membr(Gv, Cv, Xz, Xp):
    Gp = float(Xp) * float(Gv)
    Gk = float(Gv) - float(Gp)
    Cp = float(Cv) * (1 - float(Xz))
    Ck = (float(Gv) * float(Cv) - float(Gp) * float(Cp)) / float(Gk)
    return Gp, Cp, Gk, Ck


def rozd(Gk, Xr):
    Gr = float(Xr) * float(Gk)
    Gs = float(Gk) - float(Gr)
    return Gr, Gs


def smes(Gr, Ck, Ci, Gv):
    Gi = float(Gv) - float(Gr)
    Cv = (float(Gi) * float(Ci) + float(Gr) * float(Ck)) / float(Gv)
    return Gi, Cv


def smes2(Gr1, Ck1, Gr2, Ck2):
    Gr = float(Gr1) + float(Gr2)
    Ck = (float(Gr1) * float(Ck1) + float(Gr2) * float(Ck2)) / float(Gr)
    return Gr, Ck


@app.route('/')
def main():
    return render_template('base.html')


@app.route('/OS1', methods=['POST', 'GET'])
def index():
    Ci = 1500
    Gv = 1
    Xz = 0.99
    Xp = 0.2
    Xr = 0.2
    Cv = 1.2 * float(Ci)
    if request.method == 'POST':
        Ci = request.form.get("Ci")
        Gv = request.form.get("Gv")
        Xz = request.form.get("Xz")
        Xp = request.form.get("Xp")
        Xr = request.form.get("Xr")

    i = 0
    while i < 100:
        Gp, Cp, Gk, Ck = membr(Gv, Cv, Xz, Xp)
        Gr, Gs = rozd(Gk, Xr)
        Gi, Cv = smes(Gr, Ck, Ci, Gv)
        i += 1

    LP = float(Gi) * float(Ci)
    RP = float(Gp) * float(Cp) + float(Gs) * float(Ck)
    delta = float(LP) - float(RP)
    return render_template("OS1.html", Ci=Ci, Gv=Gv, Xz=Xz, Xp=Xp, Xr=Xr, Cv=Cv, Gp=Gp, Cp=Cp, Gk=Gk,
                           Ck=Ck, Gr=Gr, Gs=Gs, Gi=Gi, LP=LP, RP=RP, delta=delta)


@app.route('/OS2', methods=['POST', 'GET'])
def OS2():
    Ci = 1500
    Gv = 1
    Xz = 0.99
    Xp = 0.2
    Xr = 0.2
    Xr2 = 0.25
    Cv1 = 1.2 * float(Ci)
    if request.method == 'POST':
        Ci = request.form.get("Ci")
        Gv = request.form.get("Gv")
        Xz = request.form.get("Xz")
        Xp = request.form.get("Xp")
        Xr = request.form.get("Xr")
        Xr2 = request.form.get("Xr2")

    i = 0
    while i < 100:
        Gp1, Cp1, Gk1, Ck1 = membr(Gv, Cv1, Xz, Xp)
        Gr1, Gs1 = rozd(Gk1, Xr)
        Gp2, Cp2, Gk2, Ck2 = membr(Gp1, Cp1, Xz, Xp)
        Gr2, Gs2 = rozd(Gk2, Xr2)
        Gi2, Cv2 = smes2(Gr1, Ck1, Gr2, Ck2)
        Gi1, Cv1 = smes(Gi2, Cv2, Ci, Gv)
        i = i + 1

    LP = float(Gi1) * float(Ci)
    RP = float(Gs1) * float(Ck1) + float(Gs2) * float(Ck2)
    delta = float(LP) - float(RP)
    return render_template("OS2.html", Ci=Ci, Gv=Gv, Xz=Xz, Xp=Xp, Xr=Xr, Xr2=Xr2, Cv1=Cv1,
                           Gp1=Gp1, Cp1=Cp1, Gk1=Gk1, Ck1=Ck1, Gr1=Gr1, Gs1=Gs1, Gp2=Gp2, Cp2=Cp2, Gk2=Gk2, Ck2=Ck2,
                           Gr2=Gr2, Gs2=Gs2, Gi2=Gi2, Cv2=Cv2, Gi1=Gi1, LP=LP, RP=RP, delta=delta)


if __name__ == "__main__":
    app.run(debug=True)