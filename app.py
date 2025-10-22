import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io

st.set_page_config(page_title="Body na kružnici", layout="centered")

# Sidebar - vstupní parametry
st.sidebar.header("Parametry kružnice")
stred_x = st.sidebar.number_input("X souřadnice středu [m]", value=0.0)
stred_y = st.sidebar.number_input("Y souřadnice středu [m]", value=0.0)
polomer = st.sidebar.number_input("Poloměr [m]", value=1.0, min_value=0.01)
pocet_bodu = st.sidebar.number_input("Počet bodů", value=8, min_value=1, step=1)
barva_bodu = st.sidebar.color_picker("Barva bodů", "#FF0000")

# Výpočet bodů na kružnici
angles = np.linspace(0, 2 * np.pi, int(pocet_bodu), endpoint=False)
x = stred_x + polomer * np.cos(angles)
y = stred_y + polomer * np.sin(angles)

# Hlavní část aplikace
st.title("Body na kružnici")
st.write(f"Zadané parametry:")
st.write(f"- Střed: ({stred_x}, {stred_y}) m")
st.write(f"- Poloměr: {polomer} m")
st.write(f"- Počet bodů: {pocet_bodu}")
st.write(f"- Barva bodů: {barva_bodu}")

# Vykreslení grafu
fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(x, y, c=barva_bodu, s=80, label='Body na kružnici')
ax.scatter(stred_x, stred_y, c="black", marker="x", s=80, label="Střed")
for i in range(len(x)):
    ax.text(x[i], y[i], str(i+1), fontsize=10, ha='right', va='bottom')
ax.set_aspect('equal')
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.grid(True)
ax.set_title("Body na kružnici")
ax.legend()

st.pyplot(fig)

# Informace o autorovi a technologiích (v samostatném okně)
if st.button("O aplikaci / O autorovi"):
    st.info("""
    **Autor:** TruMartin  
    **Kontakt:** martin.tru@email.cz  
    **Použité technologie:** Python, Streamlit, Matplotlib, NumPy  
    **Popis:**  
    Tato aplikace umožňuje zobrazit a exportovat body na kružnici podle zadaných parametrů. Všechny hodnoty jsou v metrech (m).  
    """)

# Export grafu do PDF včetně parametrů úlohy, autora atd.
if st.button("Exportovat do PDF"):
    buffer = io.BytesIO()
    with PdfPages(buffer) as pdf:
        # První stránka - graf
        pdf.savefig(fig)
        # Druhá stránka - info
        plt.figure(figsize=(8.3, 11.7))
        plt.axis('off')
        info_text = (
            f"Parametry úlohy:\n"
            f"Střed: ({stred_x}, {stred_y}) m\n"
            f"Poloměr: {polomer} m\n"
            f"Počet bodů: {pocet_bodu}\n"
            f"Barva bodů: {barva_bodu}\n\n"
            "Autor: TruMartin\n"
            "Kontakt: martin.tru@email.cz\n"
            "Použité technologie: Python, Streamlit, Matplotlib, NumPy\n"
        )
        plt.text(0.5, 0.5, info_text, fontsize=14, ha='center', va='center', wrap=True)
        pdf.savefig()
    st.download_button(
        label="Stáhnout PDF",
        data=buffer.getvalue(),
        file_name="kruznice.pdf",
        mime="application/pdf"
    )
