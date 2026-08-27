import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="UEFA Şampiyonlar Ligi Kura Çekimi", layout="wide")

st.title("🏆 2026-27 UEFA Şampiyonlar Ligi Kura Simülasyonu")
st.write("Aşağıdaki butona basarak UEFA kurallarına uygun kura çekimini başlatabilirsiniz.")

def get_pots():
    return {
        1: [
            {"id": "PSG", "name": "Paris Saint-Germain", "country": "Fransa"},
            {"id": "BAY", "name": "Bayern München", "country": "Almanya"},
            {"id": "RMA", "name": "Real Madrid", "country": "İspanya"},
            {"id": "LIV", "name": "Liverpool", "country": "İngiltere"},
            {"id": "INT", "name": "Internazionale", "country": "İtalya"},
            {"id": "MCI", "name": "Manchester City", "country": "İngiltere"},
            {"id": "ARS", "name": "Arsenal", "country": "İngiltere"},
            {"id": "BAR", "name": "Barcelona", "country": "İspanya"},
            {"id": "ATM", "name": "Atlético Madrid", "country": "İspanya"}
        ],
        2: [
            {"id": "BVB", "name": "Borussia Dortmund", "country": "Almanya"},
            {"id": "ROM", "name": "Roma", "country": "İtalya"},
            {"id": "SPO", "name": "Sporting CP", "country": "Portekiz"},
            {"id": "AVL", "name": "Aston Villa", "country": "İngiltere"},
            {"id": "POR", "name": "Porto", "country": "Portekiz"},
            {"id": "MUN", "name": "Manchester United", "country": "İngiltere"},
            {"id": "BRU", "name": "Club Brugge", "country": "Belçika"},
            {"id": "BET", "name": "Real Betis", "country": "İspanya"},
            {"id": "PSV", "name": "PSV Eindhoven", "country": "Hollanda"}
        ],
        3: [
            {"id": "FEY", "name": "Feyenoord", "country": "Hollanda"},
            {"id": "LIL", "name": "Lille", "country": "Fransa"},
            {"id": "BOD", "name": "Bodø/Glimt", "country": "Norveç"},
            {"id": "NAP", "name": "Napoli", "country": "İtalya"},
            {"id": "RBL", "name": "RB Leipzig", "country": "Almanya"},
            {"id": "VIL", "name": "Villarreal", "country": "İspanya"},
            {"id": "FB",  "name": "Fenerbahçe", "country": "Türkiye"},
            {"id": "SHA", "name": "Şahtar Donetsk", "country": "Ukrayna"},
            {"id": "GS",  "name": "Galatasaray", "country": "Türkiye"}
        ],
        4: [
            {"id": "SLA", "name": "Slavia Praha", "country": "Çekya"},
            {"id": "SLO", "name": "Slovan Bratislava", "country": "Slovakya"},
            {"id": "STU", "name": "Stuttgart", "country": "Almanya"},
            {"id": "AEK", "name": "AEK Atina", "country": "Yunanistan"},
            {"id": "LAS", "name": "LASK", "country": "Avusturya"},
            {"id": "COM", "name": "Como", "country": "İtalya"},
            {"id": "LEN", "name": "Lens", "country": "Fransa"},
            {"id": "VIK", "name": "Viking", "country": "Norveç"},
            {"id": "SAB", "name": "Sabah", "country": "Azerbaycan"}
        ]
    }

def draw_simulation():
    pots = get_pots()
    all_teams = {}
    for p, teams in pots.items():
        for t in teams:
            t['pot'] = p
            all_teams[t['id']] = t

    max_attempts = 1000
    for attempt in range(max_attempts):
        home_opponents = {t_id: {} for t_id in all_teams}
        away_opponents = {t_id: {} for t_id in all_teams}
        all_opponents = {t_id: set() for t_id in all_teams}
        country_counts = {t_id: Counter() for t_id in all_teams}

        failed = False
        pot_pairs = [
            (1, 1), (2, 2), (3, 3), (4, 4),
            (1, 2), (1, 3), (1, 4),
            (2, 3), (2, 4),
            (3, 4)
        ]

        for p1, p2 in pot_pairs:
            teams_p1 = [t['id'] for t in pots[p1]]
            teams_p2 = [t['id'] for t in pots[p2]]

            if p1 == p2:
                success = False
                for _ in range(200):
                    shuffled = teams_p1[:]
                    random.shuffle(shuffled)
                    valid = True

                    for i, u in enumerate(teams_p1):
                        v = shuffled[i]
                        if u == v or all_teams[u]['country'] == all_teams[v]['country'] or v in all_opponents[u]:
                            valid = False; break
                        if country_counts[u][all_teams[v]['country']] >= 2 or country_counts[v][all_teams[u]['country']] >= 2:
                            valid = False; break
                        v_idx = teams_p1.index(v)
                        if shuffled[v_idx] == u:
                            valid = False; break

                    if valid:
                        for i, u in enumerate(teams_p1):
                            v = shuffled[i]
                            home_opponents[u][p1] = v
                            away_opponents[v][p1] = u
                            all_opponents[u].add(v)
                            all_opponents[v].add(u)
                            country_counts[u][all_teams[v]['country']] += 1
                            country_counts[v][all_teams[u]['country']] += 1
                        success = True
                        break

                if not success: failed = True; break

            else:
                success = False
                for _ in range(300):
                    shuffled_f = teams_p2[:]
                    shuffled_g = teams_p1[:]
                    random.shuffle(shuffled_f)
                    random.shuffle(shuffled_g)

                    valid = True
                    temp_counts = {t_id: Counter() for t_id in all_teams}

                    for i, u in enumerate(teams_p1):
                        v = shuffled_f[i]
                        if all_teams[u]['country'] == all_teams[v]['country'] or v in all_opponents[u]:
                            valid = False; break
                        if country_counts[u][all_teams[v]['country']] >= 2 or country_counts[v][all_teams[v]['country']] >= 2:
                            valid = False; break
                        temp_counts[u][all_teams[v]['country']] += 1
                        temp_counts[v][all_teams[u]['country']] += 1

                    if not valid: continue

                    for j, v in enumerate(teams_p2):
                        u_g = shuffled_g[j]
                        if all_teams[v]['country'] == all_teams[u_g]['country'] or u_g in all_opponents[v]:
                            valid = False; break
                        if shuffled_f[teams_p1.index(u_g)] == v:
                            valid = False; break
                        if country_counts[v][all_teams[u_g]['country']] + temp_counts[v][all_teams[u_g]['country']] >= 2 or \
                           country_counts[u_g][all_teams[v]['country']] + temp_counts[u_g][all_teams[v]['country']] >= 2:
                            valid = False; break
                        temp_counts[v][all_teams[u_g]['country']] += 1
                        temp_counts[u_g][all_teams[v]['country']] += 1

                    if valid:
                        for i, u in enumerate(teams_p1):
                            v = shuffled_f[i]
                            home_opponents[u][p2] = v
                            away_opponents[v][p1] = u
                            all_opponents[u].add(v)
                            all_opponents[v].add(u)
                            country_counts[u][all_teams[v]['country']] += 1
                            country_counts[v][all_teams[u]['country']] += 1

                        for j, v in enumerate(teams_p2):
                            u_g = shuffled_g[j]
                            home_opponents[v][p1] = u_g
                            away_opponents[u_g][p2] = v
                            all_opponents[v].add(u_g)
                            all_opponents[u_g].add(v)
                            country_counts[v][all_teams[u_g]['country']] += 1
                            country_counts[u_g][all_teams[v]['country']] += 1

                        success = True
                        break

                if not success: failed = True; break

        if not failed:
            return home_opponents, away_opponents, all_teams, pots
    return None, None, None, None

if st.button("🎲 Kura Çek", type="primary", use_container_width=True):
    with st.spinner("Kura çekiliyor..."):
        home, away, all_teams, pots = draw_simulation()
        
    if home:
        st.success("Kura Çekimi Tamamlandı!")
        for pot_num in range(1, 5):
            st.header(f"📌 {pot_num}. Torba Takımları")
            cols = st.columns(3)
            for idx, team in enumerate(pots[pot_num]):
                t_id = team['id']
                col = cols[idx % 3]
                with col:
                    with st.expander(f"⚽ {team['name']} ({team['country']})"):
                        st.markdown("**🏠 İç Saha Maçları:**")
                        for p in range(1, 5):
                            opp = all_teams[home[t_id][p]]
                            st.write(f"- Torba {p}: **{opp['name']}** ({opp['country']})")
                        st.markdown("**✈️ Deplasman Maçları:**")
                        for p in range(1, 5):
                            opp = all_teams[away[t_id][p]]
                            st.write(f"- Torba {p}: **{opp['name']}** ({opp['country']})")
    else:
        st.error("Kura hesaplanamadı, lütfen tekrar butonuna basın.")
