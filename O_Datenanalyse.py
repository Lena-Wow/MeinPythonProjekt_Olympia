import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Titel
st.title("Olympische Spiele – Körperdatenanalyse")
st.markdown(
    "Lade eine CSV-Datei hoch, um Gewicht, Größe und BMI nach Sportart und Jahr zu analysieren."
)

#  eine Funktion von Streamlit, mit der man  eine Schaltfläche für den Datei-Upload einfügt.
uploaded_file = st.file_uploader("📂 CSV-Datei hochladen", type=["csv"])

# Diese Zeile prüft: "Wurde überhaupt eine Datei hochgeladen?" Wenn nein, wird Block mit "else:  st.info("Bitte lade zuerst eine CSV-Datei hoch.")"ausgegeben"
if uploaded_file is not None:
    # Versucht, die Datei mit Pandas(pd) zu lesen und zu verarbeiten. sep=None + engine="python" erlaubt automatisches Erkennen des Trennzeichens (Komma, Semikolon etc.).
    # encoding="ISO-8859-1" ist für viele europäische Zeichensätze geeignet (z.B. deutsche Umlaute).
    try:
        df = pd.read_csv(
            uploaded_file, sep=None, engine="python", encoding="ISO-8859-1"
        )
        df.columns = (
            df.columns.str.strip()
        )  # Spaltennamen säubern, Entfernt Leerzeichen am Anfang und Ende der Spaltennamen (z. B. " Gewicht " → "Gewicht").

        # Iteriert über die drei numerischen Spalten: Gewicht, Groesse und BMI, wandel die in str um, ersetz KOmma durch punkt, und wandel die dann in float wieder
        for col in ["Gewicht in kg", "Groesse in cm", "BMI"]:
            df[col] = df[col].astype(str).str.replace(",", ".").astype(float)
        # pandas wandelt die Spalte Jahr in zahlen um. WEnn eintrag ungültig ist, wird es zu "not a number".  "coerce" bedeutet "erzwingen.Bei fehlende eingaben kann man trotzdem arbeiten.
        df["Olympic_Jahr"] = pd.to_numeric(df["Olympic_Jahr"], errors="coerce")

        # Auswahlfelder
        metriken = ["Gewicht in kg", "Groesse in cm", "BMI"]
        ausgewählte_metrik = st.selectbox(
            "Wähle ein Parameter Gewicht, Groesse oder gerechnetes BMI Index:", metriken
        )
        sportarten = df[
            "Sportart"
        ].unique()  # Funktion gibt jede Sportart nur einmal zurück, ohne Wiederholungen.
        ausgewählte_sportart = st.selectbox("Wähle eine Sportart:", sorted(sportarten))

        # Daten filtern, Filtert den DataFrame so, dass nur Einträge zur gewählten Sportart enthalten sind. D.h. Es wird nur die Zeilen ausgegebne,
        # wo die Bedeutung, bei dem Vergleich  True ist und nur die Daten(Gewicht, Groesse und BMI nur von diesem Sportart ausgewählt sind)
        df_sport = df[df["Sportart"] == ausgewählte_sportart]

        # Diagramm
        st.subheader(
            f"{ausgewählte_metrik} über die Jahre im Sport– {ausgewählte_sportart}"
        )
        fig, ax = (
            plt.subplots()
        )  # ein leeres Diagramm (Figure) und eine Zeichenfläche (Axes) wird  mit matplotlib erstellt. FIG ist Diagramm, AX ist Koordinatensystem
        ax.plot(
            df_sport["Olympic_Jahr"], df_sport[ausgewählte_metrik], marker="o"
        )  # x: Olympic_jahr,y: ausgewähler Parameter/Metrik, marker: Datenknickpunkt, kann was anderes sein
        ax.set_xlabel("Jahr")  # Beschriftung zu achse x
        ax.set_ylabel(ausgewählte_metrik)  ## Beschriftung zu achse y
        ax.set_title(f"{ausgewählte_metrik} im Zeitverlauf")  # Title über Diagramm
        ax.grid(True)  # gitternetz wird aktiviert
        st.pyplot(fig)  # wird geprintet

    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der Datei: {e}")
else:
    st.info("Bitte lade zuerst eine CSV-Datei hoch.")
