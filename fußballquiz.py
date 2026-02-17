import streamlit as st
import random
import json
import os

# ==============================
# KONFIGURATION
# ==============================
st.set_page_config(page_title="Bundesliga Quiz 2025/26", page_icon="⚽", layout="centered")
HIGHSCORE_FILE = "highscores.json"

# ==============================
# HIGHSCORE FUNKTIONEN
# ==============================
def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return {"player": [], "stadium": [], "trainer": []}
    with open(HIGHSCORE_FILE, "r") as f:
        return json.load(f)

def save_highscore(mode, name, score):
    highscores = load_highscores()
    highscores[mode].append({"name": name, "score": score})
    highscores[mode] = sorted(highscores[mode], key=lambda x: x["score"], reverse=True)[:5]
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f)

# ==============================
# DATEN
# ==============================
teams = {
    "FC Bayern München": {
        "players": ["Manuel Neuer", "Sven Ulreich", "Joshua Kimmich", "Leon Goretzka",
                    "Jamal Musiala", "Leroy Sané", "Serge Gnabry", "Kingsley Coman",
                    "Harry Kane", "Dayot Upamecano", "Min-jae Kim", "Alphonso Davies",
                    "Thomas Müller", "Konrad Laimer", "Matthijs de Ligt"],
        "stadium": "Allianz Arena",
        "trainer": "Julian Nagelsmann"
    },
    "Borussia Dortmund": {
        "players": ["Gregor Kobel", "Mats Hummels", "Julian Brandt", "Marco Reus",
                    "Karim Adeyemi", "Donyell Malen", "Emre Can", "Niclas Füllkrug",
                    "Sebastian Haller", "Salih Özcan", "Nico Schlotterbeck",
                    "Julien Duranville", "Felix Nmecha", "Youssoufa Moukoko", "Ramy Bensebaini"],
        "stadium": "Signal Iduna Park",
        "trainer": "Edin Terzic"
    },
    "RB Leipzig": {
        "players": ["Peter Gulacsi", "Willi Orban", "Xavi Simons", "Dani Olmo",
                    "Benjamin Sesko", "Lois Openda", "Christoph Baumgartner",
                    "Kevin Kampl", "David Raum", "Castello Lukeba",
                    "Mohamed Simakan", "Amadou Haidara", "Eljif Elmas",
                    "Lukas Klostermann", "Yussuf Poulsen"],
        "stadium": "Red Bull Arena",
        "trainer": "Marco Rose"
    },
    "Eintracht Frankfurt": {
        "players": ["Kevin Trapp", "Mario Götze", "Randal Kolo Muani",
                    "Hugo Ekitike", "Ansgar Knauff", "Ellyes Skhiri",
                    "Robin Koch", "Philipp Max", "Tuta", "Farès Chaïbi",
                    "Omar Marmoush", "Junior Dina Ebimbe", "Makoto Hasebe",
                    "Kristijan Jakic", "Aurélio Buta"],
        "stadium": "Deutsche Bank Park",
        "trainer": "Oliver Glasner"
    },
    "Hamburger SV": {
        "players": ["Daniel Heuer Fernandes", "Sebastian Schonlau",
                    "Ludovit Reis", "Robert Glatzel", "Bakery Jatta",
                    "Laszlo Benes", "Miro Muheim", "Jonas Meffert",
                    "Jean-Luc Dompé", "Noah Katterbach",
                    "Anssi Suhonen", "Ransford Königsdörffer",
                    "Valon Zumberi", "Ignace Van der Brempt", "Tom Sanne"],
        "stadium": "Volksparkstadion",
        "trainer": "Tim Walter"
    },
    "1. FC Köln": {
        "players": ["Marvin Schwäbe", "Timo Hübers", "Florian Kainz",
                    "Davie Selke", "Dejan Ljubicic", "Luca Waldschmidt",
                    "Jan Thielmann", "Eric Martel", "Dominique Heintz",
                    "Denis Huseinbasic", "Leart Paqarada",
                    "Steffen Tigges", "Max Finkgräfe",
                    "Damion Downs", "Mathias Olesen"],
        "stadium": "RheinEnergieStadion",
        "trainer": "Steffen Baumgart"
    },
    "Borussia Mönchengladbach": {
        "players": ["Jonas Omlin", "Alassane Plea", "Florian Neuhaus",
                    "Julian Weigl", "Joe Scally", "Rocco Reitz",
                    "Ko Itakura", "Nico Elvedi", "Tomas Cvancara",
                    "Franck Honorat", "Patrick Herrmann",
                    "Stefan Lainer", "Grant-Leon Ranos",
                    "Nathan Ngoumou", "Christoph Kramer"],
        "stadium": "Borussia-Park",
        "trainer": "Dieter Hecking"
    },
    "Bayer 04 Leverkusen": {
        "players": ["Lukas Hradecky", "Florian Wirtz", "Victor Boniface",
                    "Jeremie Frimpong", "Alejandro Grimaldo",
                    "Jonathan Tah", "Robert Andrich", "Exequiel Palacios",
                    "Adam Hlozek", "Edmond Tapsoba",
                    "Amine Adli", "Jonas Hofmann",
                    "Patrik Schick", "Piero Hincapie", "Granit Xhaka"],
        "stadium": "BayArena",
        "trainer": "Gerardo Seoane"
    },
    "FC St. Pauli": {
        "players": ["Nikola Vasilj", "Eric Smith", "Jackson Irvine",
                    "Marcel Hartel", "Oladapo Afolayan",
                    "Johannes Eggestein", "Karol Mets",
                    "Leart Paqarada Jr", "Etienne Amenyido",
                    "Connor Metcalfe", "Philipp Treu",
                    "David Nemeth", "Lars Ritzka",
                    "Maurides", "Manolis Saliakas"],
        "stadium": "Millerntor-Stadion",
        "trainer": "Timo Schultz"
    }
}

all_teams = list(teams.keys())

# ==============================
# QUIZ FUNKTIONEN
# ==============================
def generate_options(correct_team):
    wrong = random.sample([t for t in all_teams if t != correct_team], 3)
    options = wrong + [correct_team]
    random.shuffle(options)
    return options

def generate_player_questions():
    pool = [(player, team) for team, data in teams.items() for player in data["players"]]
    selected = random.sample(pool, 10)
    return [{"question": player, "correct_team": team, "options": generate_options(team)} for player, team in selected]

def generate_stadium_questions():
    pool = [(data["stadium"], team) for team, data in teams.items()]
    selected = random.sample(pool, min(10, len(pool)))
    return [{"question": stadium, "correct_team": team, "options": generate_options(team)} for stadium, team in selected]

def generate_trainer_questions():
    pool = [(data["trainer"], team) for team, data in teams.items()]
    selected = random.sample(pool, min(10, len(pool)))
    return [{"question": trainer, "correct_team": team, "options": generate_options(team)} for trainer, team in selected]

def reset_quiz(mode):
    st.session_state.mode = mode
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.finished = False
    if mode == "player":
        st.session_state.questions = generate_player_questions()
    elif mode == "stadium":
        st.session_state.questions = generate_stadium_questions()
    else:
        st.session_state.questions = generate_trainer_questions()

# ==============================
# SESSION STATE INIT
# ==============================
if "mode" not in st.session_state:
    st.session_state.mode = None

# ==============================
# STARTSEITE MIT HIGHSCORES
# ==============================
if st.session_state.mode is None:
    st.title("⚽ Bundesliga Quiz 2025/26")
    col1, col2, col3 = st.columns(3)
    if col1.button("👤 Spieler → Verein"):
        reset_quiz("player")
        st.rerun()
    if col2.button("🏟️ Stadion → Verein"):
        reset_quiz("stadium")
        st.rerun()
    if col3.button("🧑‍💼 Trainer → Verein"):
        reset_quiz("trainer")
        st.rerun()

    st.divider()
    st.subheader("🏆 Top 5 Highscores")
    highscores = load_highscores()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 👤 Spieler-Quiz")
        for entry in highscores["player"]:
            st.write(f"{entry['name']} – {entry['score']}")
    with col2:
        st.markdown("### 🏟 Stadion-Quiz")
        for entry in highscores["stadium"]:
            st.write(f"{entry['name']} – {entry['score']}")
    with col3:
        st.markdown("### 🧑‍💼 Trainer-Quiz")
        for entry in highscores["trainer"]:
            st.write(f"{entry['name']} – {entry['score']}")
    st.stop()

# ==============================
# QUIZ
# ==============================
if st.session_state.finished:
    st.subheader(f"🏁 Dein Ergebnis: {st.session_state.score}/{len(st.session_state.questions)}")
    name = st.text_input("Name für die Bestenliste:")
    if st.button("Speichern"):
        if name:
            save_highscore(st.session_state.mode, name, st.session_state.score)
            st.success("Gespeichert!")
            st.session_state.mode = None
            st.rerun()
    st.stop()

current = st.session_state.questions[st.session_state.index]
question = current["question"]
correct = current["correct_team"]
options = current["options"]

st.progress(st.session_state.index / len(st.session_state.questions))
if st.session_state.mode == "player":
    st.subheader(f"Bei welchem Verein spielt **{question}**?")
elif st.session_state.mode == "stadium":
    st.subheader(f"Zu welchem Verein gehört das Stadion **{question}**?")
else:
    st.subheader(f"Zu welchem Verein gehört der Trainer **{question}**?")

for option in options:
    color = "secondary"
    if st.session_state.answered:
        if option == correct:
            color = "primary"
        elif option == st.session_state.selected:
            color = "danger"
    if st.button(option, key=option + str(st.session_state.index), disabled=st.session_state.answered, type=color):
        st.session_state.selected = option
        st.session_state.answered = True
        if option == correct:
            st.session_state.score += 1
        st.rerun()

if st.session_state.answered:
    if st.button("➡️ Nächste Frage"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.selected = None
        if st.session_state.index >= len(st.session_state.questions):
            st.session_state.finished = True
        st.rerun()
