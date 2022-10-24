

from flask import Flask, Response, jsonify
from flask_cors import cross_origin

import pandas as pd
from chamber_hyejin import value_print_2
app = Flask(__name__)

df = pd.read_csv("data/control_rules.csv")
df["season_level"] = df["season"] + " " + df["level"]
print(df.head())


@app.route("/msg_growth")
@cross_origin(origin='*')
def msg_growth():
    # select_season = random.choice(["여름", "겨울", "비"])
    # select_level = random.choice(["1단계", "2단계", "3-1단계", "3-2단계", "4단계", "5단계"])
    #
    # msg_growth_str = "겨울 5단계"
    # msg_growth_str = f"{select_season} {select_level}"
    msg_growth_str = value_print_2.msg_growth

    #              document.getElementById("toggle-demo").checked = true;
    #              document.getElementById("win_btn").checked = false;
    #              document.getElementById("light_btn").checked = true;
    #              document.getElementById("fog_btn").checked = false;
    #              document.getElementById("co2_btn").checked = true;
    #              document.getElementById("heater_btn").checked = false;
    #              document.getElementById("o2").checked = false;
    #              document.getElementById("water_btn").checked = true;


    record = df[df["season_level"] == msg_growth_str]

    resp = {
        "name": msg_growth_str,
        "toggle-demo": record["fan"].item(),
        "win_btn": record["window"].item(),
        "light_btn": record["light"].item(),
        "fog_btn": record["fog"].item(),
        "co2_btn": record["co2"].item(),
        "heater_btn": record["heat"].item(),
        "o2_btn": record["o2"].item(),
        "water_btn": record["water"].item(),
    }

    print(resp)

    return jsonify(resp)

app.run(host="0.0.0.0", threaded=True, debug=True)
# msg_growth()