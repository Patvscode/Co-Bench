import streamlit as st
import json
import os

# ---------- Workspace State ----------
STATE_FILE = os.path.join(os.path.dirname(__file__), 'workspace', 'state.json')

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Failed to load state: {e}")
    return {"modules": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# ---------- UI ----------
st.set_page_config(page_title="Co‑Bench Workspace", layout="wide")
st.title("🎈 Co‑Bench: Generative Co‑Workspace")

state = load_state()

# Sidebar: Module manager
with st.sidebar:
    st.header("Modules")
    new_name = st.text_input("Add new module name")
    if st.button("Add Module") and new_name:
        state["modules"].append({"name": new_name, "config": {}})
        st.success(f"Module '{new_name}' added.")
    st.subheader("Current Modules")
    for i, mod in enumerate(state["modules"]):
        st.text(f"{i+1}. {mod['name']}")
    if st.button("Save Workspace"):
        save_state(state)
        st.success("Workspace saved.")

# Main area: display modules
st.subheader("Workspace Modules")
if not state["modules"]:
    st.info("No modules added yet. Use the sidebar to add some.")
else:
    for mod in state["modules"]:
        st.markdown(f"### {mod['name']}")
        st.write("(Module UI would go here.)")

# Footer note
st.caption("State is persisted in `workspace/state.json`. Changes are saved with the 'Save Workspace' button.")

