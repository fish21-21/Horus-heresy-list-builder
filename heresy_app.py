# heresy_app.py
import streamlit as st
from io import StringIO

# -----------------------------
# Data classes (unchanged logic)
# -----------------------------
class Unit:
    def __init__(self, name, points, category):
        self.name = name
        self.points = points
        self.category = category

    def __str__(self):
        return f"{self.name} ({self.points} pts)"

class ArmyList:
    def __init__(self, faction, points_limit):
        self.faction = faction
        self.points_limit = points_limit
        self.units = []

    def add_unit(self, unit):
        if self.total_points() + unit.points <= self.points_limit:
            self.units.append(unit)
            return True, f"✅ Added {unit.name} ({unit.points} pts)"
        else:
            return False, f"⚠️ Cannot add {unit.name} — would exceed points limit!"

    def total_points(self):
        return sum(u.points for u in self.units)

    def display_text(self):
        buf = StringIO()
        buf.write(f"{self.faction} Army List\n")
        buf.write(f"Points: {self.total_points()} / {self.points_limit}\n\n")
        if not self.units:
            buf.write("No units added yet.\n")
            return buf.getvalue()
        categories = {}
        for u in self.units:
            categories.setdefault(u.category, []).append(u)
        for cat, units in categories.items():
            buf.write(f"{cat}:\n")
            for u in units:
                buf.write(f" - {u.name} ({u.points} pts)\n")
            buf.write("\n")
        return buf.getvalue()

# -----------------------------
# Unit index (as you provided)
# -----------------------------
unit_index = {
    "HQ": [
        Unit("Legion Praetor", 120, "HQ"),
        Unit("Legion Cataphractii Praetor", 135, "HQ"),
        Unit("Legion Tartaros Praetor", 110, "HQ"),
        Unit("Legion Centurion", 60, "HQ"),
        Unit("Legion Cataphractii Centurion", 85, "HQ"),
        Unit("Legion Tartaros Centurion", 75, "HQ"),
        Unit("Legion Command Squad", 85, "HQ"),
        Unit("Legion Cataphractii Command Squad", 125, "HQ"),
        Unit("Legion Tartaros Command Squad", 110, "HQ"),
        Unit("Legion Damocles Command Rhino", 150, "HQ"),
    ],

    "Troops & Transports": [
        Unit("Tactical Squad (10)", 100, "Troops & Transports"),
        Unit("Despoiler Squad (10)", 100, "Troops & Transports"),
        Unit("Assault Squad (10)", 145, "Troops & Transports"),
        Unit("Breacher Squad (10)", 155, "Troops & Transports"),
        Unit("Tactical support squad (5)", 85, "Troops & Transports"),
        Unit("Scout Squad (5)", 65, "Troops & Transports"),
        Unit("Rhino Transport", 35, "Troops & Transports"),
        Unit("Drop pod", 35, "Troops & Transports"),
        Unit("Dreadnought Drop pod", 100, "Troops & Transports"),
        Unit("Termite Assult Drill", 80, "Troops & Transports"),
    ],

    "Elites": [
        Unit("Legion veteran squad", 115, "Elites"),
        Unit("Cataphractii Terminator Squad (5)", 175, "Elites"),
        Unit("Tartaros Terminator Squad (5)", 150, "Elites"),
        Unit("destroyer assult squad", 130, "Elites"),
        Unit("Mortalis Destroyer Squad", 105, "Elites"),
        Unit("Apothecarion detachment", 45, "Elites"),
        Unit("Techmarine Covenant", 55, "Elites"),
        Unit("Contemptor Dreadnought Talon", 175, "Elites"),
        Unit("Rapier Battery", 40, "Elites"),
    ],

    "Fast Attack": [
        Unit("Seeker Squad", 105, "Fast Attack"),
        Unit("Outrider Squadron", 85, "Fast Attack"),
        Unit("Sabre Strike Squadron", 80, "Fast Attack"),
        Unit("Sky-hunter Squadron", 105, "Fast Attack"),
        Unit("Javelin Squadron", 90, "Fast Attack"),
        Unit("Protues Land Raider Squadron", 60, "Fast Attack"),
        Unit("Storm Eagle Gunship", 210, "Fast Attack"),
        Unit("Xiphon Interceptor", 105, "Fast Attack"),
        Unit("Dreadclaw Drop Pod", 115, "Fast Attack"),
    ],

    "Heavy Support": [
        Unit("Leviathan Dreadnought Talon", 270, "Heavy Support"),
        Unit("Deredeo Dreadnought Talon", 205, "Heavy Support"),
        Unit("Heavy Support Squad (5)", 100, "Heavy Support"),
        Unit("Predator Squadron", 120, "Heavy Support"),
        Unit("Sicarian Squadron", 190, "Heavy Support"),
        Unit("Sicarian Aecus Squadron", 215, "Heavy Support"),
        Unit("Sicarian Punisher Squadron", 190, "Heavy Support"),
        Unit("Sicarian Venator Squadron", 200, "Heavy Support"),
        Unit("Sicarian Omega Squadron", 230, "Heavy Support"),
        Unit("Kratos Squadron", 300, "Heavy Support"),
        Unit("Land Raider Proteus Carrier Squadron", 220, "Heavy Support"),
        Unit("Land Raider Proteus Explorator", 0, "Heavy Support"),
        Unit("Vindicator Squadron", 120, "Heavy Support"),
        Unit("Land Raider Spartan", 350, "Heavy Support"),
        Unit("Scorpius Squadron", 120, "Heavy Support"),
        Unit("Arquitor Squadron", 200, "Heavy Support"),
        Unit("Fire Raptor Gunship", 280, "Heavy Support"),
        Unit("Deathstorm Drop Pod Squadron", 90, "Heavy Support"),
        Unit("Kharydis Assult Claw", 235, "Heavy Support"),
    ],
}

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Horus Heresy List Builder", layout="centered")
st.title("⚔️ Horus Heresy List Builder (Space Marines)")

# create/reset army
if "army" not in st.session_state:
    st.session_state.army = None

left, right = st.columns(2)
with left:
    if st.session_state.army is None:
        faction = st.text_input("Enter Legion / Faction name", value="Space Marines")
        points_limit = st.number_input("Points limit", min_value=100, max_value=10000, value=2000, step=50)
        if st.button("Create Army"):
            st.session_state.army = ArmyList(faction, points_limit)
            st.success(f"Army created: {faction} ({points_limit} pts)")
    else:
        if st.button("Reset Army"):
            st.session_state.army = None
            st.warning("Army reset.")

with right:
    if st.session_state.army is not None:
        st.write(f"**{st.session_state.army.faction}** — {st.session_state.army.total_points()}/{st.session_state.army.points_limit} pts")

st.markdown("---")

# If an army exists, show add controls
if st.session_state.army is not None:
    army = st.session_state.army

    # Category and unit selection
    category = st.selectbox("Category", list(unit_index.keys()))
    # show human-readable names but return Unit objects
    unit_option = st.selectbox("Unit", unit_index[category], format_func=lambda u: str(u))

    # Add / undo functionality
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Add Unit"):
            ok, msg = army.add_unit(unit_option)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    with col2:
        if st.button("Undo last add"):
            if army.units:
                removed = army.units.pop()
                st.info(f"Removed last unit: {removed.name} ({removed.points} pts)")
            else:
                st.warning("No units to remove.")
    with col3:
        if st.button("Clear list"):
            army.units.clear()
            st.warning("All units removed from army.")

    st.markdown("---")
    # show list and provide download
    st.subheader("Army list")
    st.text_area("Preview", value=army.display_text(), height=280)

    # download the list as .txt
    army_text = army.display_text()
    st.download_button(label="Download army (.txt)", data=army_text, file_name=f"{army.faction}_army.txt", mime="text/plain")

else:
    st.info("Create an army first (top-left).")

# Footer quick tips
st.markdown("---")
st.caption("Tip: add this page to your phone home screen for quick mobile access. Deploy the file to Streamlit Cloud or Replit for a public URL.")
