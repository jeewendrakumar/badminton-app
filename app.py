import streamlit as st
import random

st.set_page_config(page_title="Badminton Session Pro", page_icon="🏸", layout="wide")

# --- Initialize State for Multi-Game Sessions ---
if 'players_stats' not in st.session_state:
    st.session_state.players_stats = {} # Format: {name: games_played}
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🏸 Badminton Smart Rotation")

# --- Sidebar: Dynamic Setup ---
with st.sidebar:
    st.header("1. Setup Players")
    input_names = st.text_area("Names (one per line):", value="Alice\nBob\nCharlie\nDave\nEve\nFrank\nGrace\nHank", height=200)
    names_list = [n.strip() for n in input_names.split('\n') if n.strip()]
    
    # Sync stats with input list
    for name in names_list:
        if name not in st.session_state.players_stats:
            st.session_state.players_stats[name] = 0

    st.divider()
    st.header("2. Setup Courts")
    n_courts = st.number_input("Number of Courts", min_value=1, value=2)
    
    court_modes = {}
    for i in range(n_courts):
        court_modes[i+1] = st.selectbox(f"Court {i+1} Mode", ["Doubles", "Singles"], key=f"mode_{i}")

    if st.button("Reset All Stats"):
        st.session_state.players_stats = {name: 0 for name in names_list}
        st.session_state.history = []
        st.rerun()

# --- Fairness Logic: The Rotator ---
def generate_next_round():
    # Sort players: fewest games played first
    available = names_list.copy()
    random.shuffle(available) # Add randomness for players with same game count
    available.sort(key=lambda x: st.session_state.players_stats[x])
    
    round_data = []
    used = set()
    
    for court, mode in court_modes.items():
        needed = 4 if mode == "Doubles" else 2
        pool = [p for p in available if p not in used]
        
        if len(pool) >= needed:
            match_players = pool[:needed]
            for p in match_players:
                used.add(p)
                st.session_state.players_stats[p] += 1
            
            round_data.append({"court": court, "mode": mode, "players": match_players})
            
    resting = [p for p in names_list if p not in used]
    return round_data, resting

# --- Main UI ---
col_left, col_right = st.columns([3, 1])

with col_left:
    if st.button("🚀 Start Next Game / Round", use_container_width=True):
        matches, rest = generate_next_round()
        st.session_state.history.append({"matches": matches, "rest": rest})

    if st.session_state.history:
        latest = st.session_state.history[-1]
        round_num = len(st.session_state.history)
        st.header(f"📍 Current Game: Round {round_num}")
        
        # Display Courts in a Grid
        grid = st.columns(min(n_courts, 3))
        for idx, m in enumerate(latest['matches']):
            with grid[idx % 3]:
                st.info(f"**Court {m['court']} ({m['mode']})**")
                p = m['players']
                if m['mode'] == "Doubles":
                    st.write(f"🏠 {p[0]} & {p[1]}")
                    st.write("🆚")
                    st.write(f"🚀 {p[2]} & {p[3]}")
                else:
                    st.write(f"🏠 {p[0]} vs 🚀 {p[1]}")

        if latest['rest']:
            st.warning(f"🥤 **Resting:** {', '.join(latest['rest'])}")

with col_right:
    st.header("📊 Total Games")
    sorted_stats = dict(sorted(st.session_state.players_stats.items(), key=lambda x: x[1], reverse=True))
    for p, count in sorted_stats.items():
        st.write(f"**{p}**: {count}")

