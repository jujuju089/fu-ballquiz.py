import streamlit as st
import random

# ==============================
# KONFIGURATION
# ==============================

st.set_page_config(page_title="Bundesliga Quiz 2025/26", page_icon="⚽", layout="centered")

# ==============================
# VEREINS-DATEN (DEIN ORIGINAL + STADIEN)
# ==============================

teams = {
    "FC Bayern München": {
        "players": [
            "Manuel Neuer", "Sven Ulreich", "Joshua Kimmich", "Leon Goretzka",
            "Jamal Musiala", "Leroy Sané", "Serge Gnabry", "Kingsley Coman",
            "Harry Kane", "Dayot Upamecano", "Min-jae Kim", "Alphonso Davies",
            "Thomas Müller", "Konrad Laimer", "Matthijs de Ligt"
        ],
        "stadium": "Allianz Arena"
    },
    "Borussia Dortmund": {
        "players": [
            "Gregor Kobel", "Mats Hummels", "Julian Brandt", "Marco Reus",
            "Karim Adeyemi", "Donyell Malen", "Emre Can", "Niclas Füllkrug",
            "Sebastian Haller", "Salih Özcan", "Nico Schlotterbeck",
            "Julien Duranville", "Felix Nmecha", "Youssoufa Moukoko", "Ramy Bensebaini"
        ],
        "stadium": "Signal Iduna Park"
    },
    "RB Leipzig": {
        "players": [
            "Peter Gulacsi", "Willi Orban", "Xavi Simons", "Dani Olmo",
            "Benjamin Sesko", "Lois Openda", "Christoph Baumgartner",
            "Kevin Kampl", "David Raum", "Castello Lukeba",
            "Mohamed Simakan", "Amadou Haidara", "Eljif Elmas",
            "Lukas Klostermann", "Yussuf Poulsen"
        ],
        "stadium": "Red Bull Arena"
    },
    "Eintracht Frankfurt": {
        "players": [
            "Kevin Trapp", "Mario Götze", "Randal Kolo Muani",
            "Hugo Ekitike", "Ansgar Knauff", "Ellyes Skhiri",
            "Robin Koch", "Philipp Max", "Tuta", "Farès Chaïbi",
            "Omar Marmoush", "Junior Dina Ebimbe", "Makoto Hasebe",
            "Kristijan Jakic", "Aurélio Buta"
        ],
        "stadium": "Deutsche Bank Park"
    },
    "Hamburger SV": {
        "players": [
            "Daniel Heuer Fernandes", "Sebastian Schonlau",
            "Ludovit Reis", "Robert Glatzel", "Bakery Jatta",
            "Laszlo Benes", "Miro Muheim", "Jonas Meffert",
            "Jean-Luc Dompé", "Noah Katterbach",
            "Anssi Suhonen", "Ransford Königsdörffer",
            "Valon Zumberi", "Ignace Van der Brempt", "Tom Sanne"
        ],
        "stadium": "Volksparkstadion"
    },
    "1. FC Köln": {
        "players": [
            "Marvin Schwäbe", "Timo Hübers", "Florian Kainz",
            "Davie Selke", "Dejan Ljubicic", "Luca Waldschmidt",
            "Jan Thielmann", "Eric Martel", "Dominique Heintz",
            "Denis Huseinbasic", "Leart Paqarada",
            "Steffen Tigges", "Max Finkgräfe",
            "Damion Downs", "Mathias Olesen"
        ],
        "stadium": "RheinEnergieStadion"
    },
    "Borussia Mönchengladbach": {
        "players": [
            "Jonas Omlin", "Alassane Plea", "Florian Neuhaus",
            "Julian Weigl", "Joe Scally", "Rocco Reitz",
            "Ko Itakura", "Nico Elvedi", "Tomas Cvancara",
            "Franck Honorat", "Patrick Herrmann",
            "Stefan Lainer", "Grant-Leon Ranos",
            "Nathan Ngoumou", "Christoph Kramer"
        ],
        "stadium": "Borussia-Park"
    },
    "Bayer 04 Leverkusen": {
        "players": [
            "Lukas Hradecky", "Florian Wirtz", "Victor Boniface",
            "Jeremie Frimpong", "Alejandro Grimaldo",
            "Jonathan Tah", "Robert Andrich", "Exequiel Palacios",
            "Adam Hlozek", "Edmond Tapsoba",
            "Amine Adli", "Jonas Hofmann",
            "Patrik Schick", "Piero Hincapie", "Granit Xhaka"
        ],
        "stadium": "BayArena"
    },
    "FC St. Pauli": {
        "players": [
            "Nikola Vasilj", "Eric Smith", "Jackson Irvine",
            "Marcel Hartel", "Oladapo Afolayan",
            "Johannes Eggestein", "Karol Mets",
            "Leart Paqarada Jr", "Etienne Amenyido",
            "Connor Metcalfe", "Philipp Treu",
            "David Nemeth", "Lars Ritzka",
            "Maurides", "Manolis Saliakas"
        ],
        "stadium": "Millerntor-Stadion"
    }
}

all_teams = list(teams.keys())

# ==============================
# FUNKTIONEN
# ==============================

def generate_options(correct_team):
    wrong = random.sample([t for t in all_teams if t != correct_team], 3)
    options = wrong + [correct_team]
    random.shuffle(options)
    return options


def generate_player_questions():
    all_players = []
    for team, data in teams.items():
        for player in data["players"]:
            all_players.append((player, team))

    selected = random.sample(all_players, 10)
    questions = []
    for player, team in selected:
        questions.append({
            "question": player,
            "correct_team": team,
            "options": generate_options(team)
        })
    return questions


def generate_stadium_questions():
    all_stadiums = []
    for team, data in teams.items():
        all_stadiums.append((data["stadium"], team))

    selected = random.sample(all_stadiums, min(10, len(all_stadiums)))
    questions = []
    for stadium, team in selected:
        questions.append({
            "question": stadium,
            "correct_team": team,
            "options": generate_options(team)
        })
    return questions


def reset_quiz(mode):
    st.session_state.mode = mode
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.quiz_finished = False

    if mode == "player":
        st.session_state.questions = generate_player_questions()
    else:
        st.session_state.questions = generate_stadium_questions()


# ==============================
# SESSION STATE
# ==============================

if "mode" not in st.session_state:
    st.session_state.mode = None

# ==============================
# STARTMENÜ
# ==============================

if st.session_state.mode is None:
    st.title("⚽ Bundesliga Quiz 2025/26")
    st.subheader("Wähle dein Quiz:")

    col1, col2 = st.columns(2)

    if col1.button("👤 Spieler → Verein"):
        reset_quiz("player")
        st.rerun()

    if col2.button("🏟️ Stadion → Verein"):
        reset_quiz("stadium")
        st.rerun()

    st.stop()

# ==============================
# QUIZ
# ==============================

if st.session_state.quiz_finished:
    st.subheader(f"🏁 Ergebnis: {st.session_state.score}/{len(st.session_state.questions)}")

    if st.button("🔄 Zurück zum Menü"):
        st.session_state.mode = None
        st.rerun()

    st.stop()

current = st.session_state.questions[st.session_state.question_index]
question = current["question"]
correct_team = current["correct_team"]
options = current["options"]

st.progress(st.session_state.question_index / len(st.session_state.questions))

if st.session_state.mode == "player":
    st.subheader(f"Bei welchem Verein spielt **{question}**?")
else:
    st.subheader(f"Zu welchem Verein gehört das Stadion **{question}**?")

selected = st.radio(
    "Wähle deine Antwort:",
    options,
    key=f"radio_{st.session_state.question_index}",
    disabled=st.session_state.answered
)

if st.button("Antwort abschicken") and not st.session_state.answered:
    st.session_state.answered = True
    if selected == correct_team:
        st.session_state.score += 1

if st.session_state.answered:
    st.write("### Lösung:")
    for option in options:
        if option == correct_team:
            st.markdown(f"🟢 **{option}** (Richtig)")
        elif option == selected:
            st.markdown(f"🔴 **{option}** (Deine Antwort)")
        else:
            st.markdown(option)

    if st.button("➡️ Nächste Frage"):
        st.session_state.question_index += 1
        st.session_state.answered = False

        if st.session_state.question_index >= len(st.session_state.questions):
            st.session_state.quiz_finished = True

        st.rerun()
