import streamlit as st
import random

# ==============================
# KONFIGURATION
# ==============================

st.set_page_config(page_title="Bundesliga Quiz 2025/26", page_icon="⚽", layout="centered")

# ==============================
# VEREINS- UND SPIELERDATEN
# (realistisch angenommene Kader 2025/26)
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
# SESSION STATE INITIALISIERUNG
# ==============================

if "question_index" not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.questions = random.sample(all_players, 10)
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.quiz_finished = False

# ==============================
# FUNKTIONEN
# ==============================

def generate_options(correct_team):
    wrong_teams = random.sample([team for team in all_teams if team != correct_team], 3)
    options = wrong_teams + [correct_team]
    random.shuffle(options)
    return options

def reset_quiz():
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.questions = random.sample(all_players, 10)
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.quiz_finished = False

# ==============================
# UI
# ==============================

st.title("⚽ Bundesliga Quiz – Saison 2025/26")
st.write("Teste dein Wissen über die Vereine der Saison 2025/26!")

# Wenn Quiz beendet
if st.session_state.quiz_finished:
    st.subheader(f"🏁 Runde beendet! Deine Punktzahl: {st.session_state.score}/10")

    if st.session_state.score <= 3:
        st.error("Kreisliga-Experte")
    elif st.session_state.score <= 7:
        st.warning("Bundesliga-Kenner")
    else:
        st.success("Transfermarkt-Profi")

    if st.button("🔄 Neue Runde starten"):
        reset_quiz()
        st.rerun()

    st.stop()

# Fortschritt
progress = st.session_state.question_index / 10
st.progress(progress)
st.write(f"Frage {st.session_state.question_index + 1} von 10")

# Aktuelle Frage
player, correct_team = st.session_state.questions[st.session_state.question_index]
options = generate_options(correct_team)

st.subheader(f"Bei welchem Verein spielt **{player}** in der Saison 2025/26?")

# Antwortauswahl
selected = st.radio("Wähle deine Antwort:", options, key=f"q_{st.session_state.question_index}")

if st.button("Antwort bestätigen") and not st.session_state.answered:
    st.session_state.answered = True
    st.session_state.selected_option = selected

    if selected == correct_team:
        st.session_state.score += 1

# Feedback anzeigen
if st.session_state.answered:
    if st.session_state.selected_option == correct_team:
        st.success("✅ Richtig!")
    else:
        st.error(f"❌ Falsch! Richtige Antwort: {correct_team}")

    if st.button("➡️ Nächste Frage"):
        st.session_state.question_index += 1
        st.session_state.answered = False
        st.session_state.selected_option = None

        if st.session_state.question_index >= 10:
            st.session_state.quiz_finished = True

        st.rerun()
