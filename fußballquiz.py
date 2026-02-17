import streamlit as st
import random

# ==============================
# KONFIGURATION
# ==============================

st.set_page_config(page_title="Bundesliga Quiz 2025/26", page_icon="⚽", layout="centered")

# ==============================
# VEREINS- UND SPIELERDATEN
# ==============================

teams = {
    "FC Bayern München": [
        "Manuel Neuer", "Sven Ulreich", "Joshua Kimmich", "Leon Goretzka",
        "Jamal Musiala", "Leroy Sané", "Serge Gnabry", "Kingsley Coman",
        "Harry Kane", "Dayot Upamecano", "Min-jae Kim", "Alphonso Davies",
        "Thomas Müller", "Konrad Laimer", "Matthijs de Ligt"
    ],
    "Borussia Dortmund": [
        "Gregor Kobel", "Mats Hummels", "Julian Brandt", "Marco Reus",
        "Karim Adeyemi", "Donyell Malen", "Emre Can", "Niclas Füllkrug",
        "Sebastian Haller", "Salih Özcan", "Nico Schlotterbeck",
        "Julien Duranville", "Felix Nmecha", "Youssoufa Moukoko", "Ramy Bensebaini"
    ],
    "RB Leipzig": [
        "Peter Gulacsi", "Willi Orban", "Xavi Simons", "Dani Olmo",
        "Benjamin Sesko", "Lois Openda", "Christoph Baumgartner",
        "Kevin Kampl", "David Raum", "Castello Lukeba",
        "Mohamed Simakan", "Amadou Haidara", "Eljif Elmas",
        "Lukas Klostermann", "Yussuf Poulsen"
    ],
    "Eintracht Frankfurt": [
        "Kevin Trapp", "Mario Götze", "Randal Kolo Muani",
        "Hugo Ekitike", "Ansgar Knauff", "Ellyes Skhiri",
        "Robin Koch", "Philipp Max", "Tuta", "Farès Chaïbi",
        "Omar Marmoush", "Junior Dina Ebimbe", "Makoto Hasebe",
        "Kristijan Jakic", "Aurélio Buta"
    ],
    "Hamburger SV": [
        "Daniel Heuer Fernandes", "Sebastian Schonlau",
        "Ludovit Reis", "Robert Glatzel", "Bakery Jatta",
        "Laszlo Benes", "Miro Muheim", "Jonas Meffert",
        "Jean-Luc Dompé", "Noah Katterbach",
        "Anssi Suhonen", "Ransford Königsdörffer",
        "Valon Zumberi", "Ignace Van der Brempt", "Tom Sanne"
    ],
    "1. FC Köln": [
        "Marvin Schwäbe", "Timo Hübers", "Florian Kainz",
        "Davie Selke", "Dejan Ljubicic", "Luca Waldschmidt",
        "Jan Thielmann", "Eric Martel", "Dominique Heintz",
        "Denis Huseinbasic", "Leart Paqarada",
        "Steffen Tigges", "Max Finkgräfe",
        "Damion Downs", "Mathias Olesen"
    ],
    "Borussia Mönchengladbach": [
        "Jonas Omlin", "Alassane Plea", "Florian Neuhaus",
        "Julian Weigl", "Joe Scally", "Rocco Reitz",
        "Ko Itakura", "Nico Elvedi", "Tomas Cvancara",
        "Franck Honorat", "Patrick Herrmann",
        "Stefan Lainer", "Grant-Leon Ranos",
        "Nathan Ngoumou", "Christoph Kramer"
    ],
    "Bayer 04 Leverkusen": [
        "Lukas Hradecky", "Florian Wirtz", "Victor Boniface",
        "Jeremie Frimpong", "Alejandro Grimaldo",
        "Jonathan Tah", "Robert Andrich", "Exequiel Palacios",
        "Adam Hlozek", "Edmond Tapsoba",
        "Amine Adli", "Jonas Hofmann",
        "Patrik Schick", "Piero Hincapie", "Granit Xhaka"
    ],
    "FC St. Pauli": [
        "Nikola Vasilj", "Eric Smith", "Jackson Irvine",
        "Marcel Hartel", "Oladapo Afolayan",
        "Johannes Eggestein", "Karol Mets",
        "Leart Paqarada Jr", "Etienne Amenyido",
        "Connor Metcalfe", "Philipp Treu",
        "David Nemeth", "Lars Ritzka",
        "Maurides", "Manolis Saliakas"
    ]
}

all_players = [(player, team) for team, players in teams.items() for player in players]
all_teams = list(teams.keys())

# ==============================
# FUNKTIONEN
# ==============================

def generate_options(correct_team):
    wrong = random.sample([t for t in all_teams if t != correct_team], 3)
    options = wrong + [correct_team]
    random.shuffle(options)
    return options


def generate_questions():
    questions = []
    for player, team in random.sample(all_players, 10):
        questions.append({
            "player": player,
            "correct_team": team,
            "options": generate_options(team)
        })
    return questions


def reset_quiz():
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.questions = generate_questions()
    st.session_state.answered = False
    st.session_state.quiz_finished = False


# ==============================
# SESSION STATE
# ==============================

if "question_index" not in st.session_state:
    reset_quiz()

# ==============================
# UI
# ==============================

st.title("⚽ Bundesliga Quiz 2025/26")

if st.session_state.quiz_finished:
    st.subheader(f"🏁 Ergebnis: {st.session_state.score}/10")

    if st.button("🔄 Neue Runde starten"):
        reset_quiz()
        st.rerun()

    st.stop()

st.progress(st.session_state.question_index / 10)

current = st.session_state.questions[st.session_state.question_index]
player = current["player"]
correct_team = current["correct_team"]
options = current["options"]

st.subheader(f"Bei welchem Verein spielt **{player}**?")

selected = st.radio(
    "Wähle deine Antwort:",
    options,
    key=f"radio_{st.session_state.question_index}",
    disabled=st.session_state.answered
)

# ==============================
# ANTWORT BESTÄTIGEN
# ==============================

if st.button("Antwort abschicken") and not st.session_state.answered:
    st.session_state.answered = True

    if selected == correct_team:
        st.session_state.score += 1

# ==============================
# FEEDBACK MIT MARKIERUNG
# ==============================

if st.session_state.answered:

    st.write("### Lösung:")

    for option in options:
        if option == correct_team:
            st.markdown(f"🟢 **{option}** (Richtig)")
        elif option == selected:
            st.markdown(f"🔴 **{option}** (Deine Antwort)")
        else:
            st.markdown(f"{option}")

    if st.button("➡️ Nächste Frage"):
        st.session_state.question_index += 1
        st.session_state.answered = False

        if st.session_state.question_index >= 10:
            st.session_state.quiz_finished = True

        st.rerun()

