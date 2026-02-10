import streamlit as st
import json
import os
import streamlit.components.v1 as components
import yaml

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

# ---------- Module Loader ----------
def load_modules():
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    loaded = {}
    if os.path.isdir(modules_dir):
        for entry in os.scandir(modules_dir):
            if entry.is_dir():
                manifest_path = os.path.join(entry.path, 'module.yaml')
                if os.path.isfile(manifest_path):
                    try:
                        with open(manifest_path, 'r') as f:
                            manifest = yaml.safe_load(f)
                        entry_point = manifest.get('entry_point')
                        ui_type = manifest.get('ui_type', 'page')
                        if entry_point:
                            module_path = os.path.join(entry.path, entry_point)
                            import importlib.util
                            spec = importlib.util.spec_from_file_location(entry.name, module_path)
                            mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(mod)
                            loaded[manifest.get('name', entry.name)] = {
                                'module': mod,
                                'ui_type': ui_type,
                                'manifest': manifest,
                            }
                    except Exception as e:
                        st.warning(f"Failed to load module {entry.name}: {e}")
    return loaded

# ---------- UI ----------
st.set_page_config(page_title="Co‑Bench Workspace", layout="wide")
st.title("🎈 Co‑Bench: Generative Co‑Workspace")

state = load_state()
modules = load_modules()
selected_module = None
if modules:
    selected_module = st.sidebar.selectbox("Run module", list(modules.keys()))

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
    st.markdown("---")
    # Mini‑app command handling
    if st.button("Status (from Mini‑App)"):
        import subprocess, shlex
        try:
            result = subprocess.check_output(shlex.split('git -C /home/pmello/.openclaw/workspace/co_bench_repo status -s'), stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = f"Error: {e.output}"
        st.code(result or "No changes.")
    if st.button("Restart (from Mini‑App)"):
        st.info("Triggering a restart of the Streamlit server (please refresh the page after a few seconds).")
        # In a real deployment you could signal a systemd service or use a watchdog.
    if st.button("Send Log (from Mini‑App)"):
        log_path = '/home/pmello/.openclaw/workspace/CO_BENCH_LOG.txt'
        try:
            with open(log_path, 'r') as f:
                log_content = f.read()
            st.text_area('Log output', log_content, height=300)
        except FileNotFoundError:
            st.warning('Log file not found.')
    # ---- Messaging the assistant ----
    st.subheader("Message the Assistant")
    user_msg = st.text_input("Your message for the assistant")
    if st.button("Send to Assistant"):
        # Write the user message to a file that the assistant can read
        msg_path = os.path.join(os.path.dirname(__file__), 'workspace', 'user_message.txt')
        with open(msg_path, 'w') as f:
            f.write(user_msg)
        st.success("Message sent. Awaiting reply…")
    # Show assistant reply if available
    reply_path = os.path.join(os.path.dirname(__file__), 'workspace', 'assistant_reply.txt')
    if os.path.exists(reply_path):
        with open(reply_path, 'r') as f:
            reply = f.read()
        st.subheader("Assistant reply")
        st.write(reply)
        # Optionally clear after showing
        # os.remove(reply_path)



# Main area: display modules
if selected_module:
    mod_info = modules[selected_module]
    st.subheader(f"Module: {selected_module}")
    # Assume the module provides a `render` function
    render_func = getattr(mod_info['module'], 'render', None)
    if callable(render_func):
        render_func()
    else:
        st.warning('Module has no render() function.')
else:
    st.subheader("Workspace Modules")
    if not state["modules"]:
        st.info("No modules added yet. Use the sidebar to add some.")
    else:
        for mod in state["modules"]:
            st.markdown(f"### {mod['name']}")
            st.write("(Module UI would go here.)")

# Footer note
st.caption("State is persisted in `workspace/state.json`. Changes are saved with the 'Save Workspace' button.")

