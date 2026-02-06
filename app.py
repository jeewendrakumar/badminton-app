import streamlit as st
import random

st.set_page_config(page_title="Badminton Pairer", page_icon="🏸")

st.title("🏸 Badminton Doubles Pairer")

# --- Sidebar for Settings ---
with st.sidebar:
    st.header("Setup")
    num_courts = st.number_input("Number of Courts", min_value=1, value=1)
    player_input = st.text_area("Enter Player Names (one per line)", 
                                value="Alice\nBob\nCharlie\nDave\nEve\nFrank")
    
# Process players
player_list = [p.strip() for p in player_input.split('\n') if p.strip()]

if st.button("Generate Random Pairings"):
    if len(player_list) < 4:
        st.error("Need at least 4 players for doubles!")
    else:
        # Shuffle players
        shuffled = player_list.copy()
        random.shuffle(shuffled)
        
        # Calculate games
        max_players_on_court = num_courts * 4
        on_court = shuffled[:max_players_on_court]
        resting = shuffled[max_players_on_court:]
        
        # Display Results
        st.subheader("Current Matches")
        cols = st.columns(min(num_courts, 3))
        
        for i in range(0, len(on_court), 4):
            court_num = (i // 4) + 1
            col_idx = (i // 4) % 3
            with cols[col_idx]:
                group = on_court[i:i+4]
                if len(group) == 4:
                    st.info(f"**Court {court_num}**")
                    st.write(f"**Team A:** {group[0]} & {group[1]}")
                    st.write("🆚")
                    st.write(f"**Team B:** {group[2]} & {group[3]}")
        
        if resting:
            st.divider()
            st.subheader("🥤 Resting This Round")
            st.write(", ".join(resting))
