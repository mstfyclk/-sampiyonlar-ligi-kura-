import random
from collections import Counter
import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="UEFA Şampiyonlar Ligi Kura Çekimi",
    layout="wide",
    page_icon="🏆",
)

# --- 🎵 ŞAMPİYONLAR LİGİ İNTRO & OTOMATİK MÜZİK ---
# 1. Orijinal Şampiyonlar Ligi Görseli
st.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/UEFA_Champions_League_logo_2021.svg/1200px-UEFA_Champions_League_logo_2021.svg.png",
    use_container_width=True,
)

# 2. Şampiyonlar Ligi Marşı (Otomatik Çalar)
st.audio(
    "https://ia801902.us.archive.org/24/items/tvtunes_6612/UEFA%20Champions%20League%20-%202004-2005.mp3",
    format="audio/mp3",
    autoplay=True,
)

# --- BAŞLIK VE MESAJLAR ---
st.title("🏆 2026-27 UEFA Şampiyonlar Ligi Kura Simülasyonu")

# 1. Turnuva ekibine özel (Büyük Harflerle)
st.info("👋 **DEVLER LİGİ KURA ÇEKİMİNE HOŞ GELDİNİZ!**")

# 2. Kura kuralları kaldırıldı.

# 3. Arkadaşlara özel gizli mesaj
with st.expander("🎁 **Arkadaşlara Özel Gizli Mesaj (Tıklamadan Geçme!)**"):
    st.write("🖕🏿")

st.write("---")
st.write(
    "Aşağıdaki kırmızı **Kura Çek** butonuna basarak kurayı başlatabilirsiniz."
)


# --- TORBALAR VE VERİ YAPISI ---
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
            {"id": "ATM", "name": "Atlético Madrid", "country": "İspanya"},
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
            {"id": "PSV", "name": "PSV Eindhoven", "country": "Hollanda"},
        ],
        3: [
            {"id": "FEY", "name": "Feyenoord", "country": "Hollanda"},
            {"id": "LIL", "name": "Lille", "country": "Fransa"},
            {"id": "BOD", "name": "Bodø/Glimt", "country": "Norveç"},
            {"id": "NAP", "name": "Napoli", "country": "İtalya"},
            {"id": "RBL", "name": "RB Leipzig", "country": "Almanya"},
            {"id": "VIL", "name": "Villarreal", "country": "İspanya"},
            {"id": "FB", "name": "Fenerbahçe", "country": "Türkiye"},
            {"id": "SHA", "name": "Şahtar Donetsk", "country": "Ukrayna"},
            {"id": "GS", "name": "Galatasaray", "country": "Türkiye"},
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
            {"id": "SAB", "name": "Sabah", "country": "Azerbaycan"},
        ],
    }


# --- KURA ALGORİTMASI ---
def draw_simulation():
    pots = get_pots()
    all_teams = {}
    for p, teams in pots.items():
        for t in teams:
            t["pot"] = p
            all_teams[t["id"]] = t

    def valid_pair(u, v, home_opps, away_opps, all_opps, c_counts, pot_u, pot_v):
        if u == v:
            return False
        if all_teams[u]["country"] == all_teams[v]["country"]:
            return False
        if v in all_opps[u]:
            return False
        if pot_v in home_opps[u]:
            return False
        if pot_u in away_opps[v]:
            return False
        if c_counts[u][all_teams[v]["country"]] >= 2:
            return False
        if c_counts[v][all_teams[u]["country"]] >= 2:
            return False
        return True

    for attempt in range(2000):
        home_opponents = {t_id: {} for t_id in all_teams}
        away_opponents = {t_id: {} for t_id in all_teams}
        all_opponents = {t_id: set() for t_id in all_teams}
        country_counts = {t_id: Counter() for t_id in all_teams}

        failed = False
        pot_pairs = [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 3),
            (2, 4),
            (3, 4),
        ]

        for p1, p2 in pot_pairs:
            teams_p1 = [t["id"] for t in pots[p1]]
            teams_p2 = [t["id"] for t in pots[p2]]

            if p1 == p2:
                success = False
                for _ in range(300):
                    shuffled = teams_p1[:]
                    random.shuffle(shuffled)
                    ok = True
                    for i, u in enumerate(teams_p1):
                        v = shuffled[i]
                        if not valid_pair(
                            u,
                            v,
                            home_opponents,
                            away_opponents,
                            all_opponents,
                            country_counts,
                            p1,
                            p1,
                        ):
                            ok = False
                            break

                    if ok:
                        for i, u in enumerate(teams_p1):
                            v = shuffled[i]
                            home_opponents[u][p1] = v
                            away_opponents[v][p1] = u
                            all_opponents[u].add(v)
                            all_opponents[v].add(u)
                            country_counts[u][all_teams[v]["country"]] += 1
                            country_counts[v][all_teams[u]["country"]] += 1
                        success = True
                        break
                if not success:
                    failed = True
                    break

            else:
                success = False
                for _ in range(500):
                    shuffled_home = teams_p2[:]
                    shuffled_away = teams_p1[:]
                    random.shuffle(shuffled_home)
                    random.shuffle(shuffled_away)

                    trial_counts = {
                        t: country_counts[t].copy() for t in all_teams
                    }
                    trial_opps = {t: set(all_opponents[t]) for t in all_teams}
                    ok = True

                    for i, u in enumerate(teams_p1):
                        v = shuffled_home[i]
                        if all_teams[u]["country"] == all_teams[v]["country"]:
                            ok = False
                            break
                        if v in trial_opps[u]:
                            ok = False
                            break
                        if trial_counts[u][all_teams[v]["country"]] >= 2:
                            ok = False
                            break
                        if trial_counts[v][all_teams[u]["country"]] >= 2:
                            ok = False
                            break
                        trial_opps[u].add(v)
                        trial_opps[v].add(u)
                        trial_counts[u][all_teams[v]["country"]] += 1
                        trial_counts[v][all_teams[u]["country"]] += 1

                    if not ok:
                        continue

                    for j, v in enumerate(teams_p2):
                        u_opp = shuffled_away[j]
                        if all_teams[v]["country"] == all_teams[u_opp]["country"]:
                            ok = False
                            break
                        if u_opp in trial_opps[v]:
                            ok = False
                            break
                        if trial_counts[v][all_teams[u_opp]["country"]] >= 2:
                            ok = False
                            break
                        if trial_counts[u_opp][all_teams[v]["country"]] >= 2:
                            ok = False
                            break
                        trial_opps[v].add(u_opp)
                        trial_opps[u_opp].add(v)
                        trial_counts[v][all_teams[u_opp]["country"]] += 1
                        trial_counts[u_opp][all_teams[v]["country"]] += 1

                    if ok:
                        for i, u in enumerate(teams_p1):
                            v = shuffled_home[i]
                            home_opponents[u][p2] = v
                            away_opponents[v][p1] = u
                            all_opponents[u].add(v)
                            all_opponents[v].add(u)
                            country_counts[u][all_teams[v]["country"]] += 1
                            country_counts[v][all_teams[u]["country"]] += 1

                        for j, v in enumerate(teams_p2):
                            u_opp = shuffled_away[j]
                            home_opponents[v][p1] = u_opp
                            away_opponents[u_opp][p2] = v
                            all_opponents[v].add(u_opp)
                            all_opponents[u_opp].add(v)
                            country_counts[v][all_teams[u_opp]["country"]] += 1
                            country_counts[u_opp][all_teams[v]["country"]] += 1

                        success = True
                        break

                if not success:
                    failed = True
                    break

        if not failed:
            return home_opponents, away_opponents, all_teams, pots

    return None, None, None, None


# --- ARAYÜZ VE KURA ÇEKİMİ ---
if st.button("🎲 Kura Çek", type="primary", use_container_width=True):
    with st.spinner("Kura çekiliyor..."):
        home, away, all_teams, pots = draw_simulation()

    if home:
        st.success("Kura Çekimi Tamamlandı!")
        for pot_num in range(1, 5):
            st.header(f"📌 {pot_num}. Torba Takımları")
            cols = st.columns(3)
            for idx, team in enumerate(pots[pot_num]):
                t_id = team["id"]
                col = cols[idx % 3]
                with col:
                    with st.expander(f"⚽ {team['name']} ({team['country']})"):
                        st.markdown("**🏠 İç Saha Maçları:**")
                        for p in range(1, 5):
                            opp = all_teams[home[t_id][p]]
                            st.write(
                                f"- Torba {p}: **{opp['name']}**"
                                f" ({opp['country']})"
                            )
                        st.markdown("**✈️ Deplasman Maçları:**")
                        for p in range(1, 5):
                            opp = all_teams[away[t_id][p]]
                            st.write(
                                f"- Torba {p}: **{opp['name']}**"
                                f" ({opp['country']})"
                            )
    else:
        st.error("Kura hesaplanamadı, lütfen tekrar butonuna basın.")
