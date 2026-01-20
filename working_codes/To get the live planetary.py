
# Code: To find the current planaetary


import swisseph as swe
import datetime

# ================================
# CONFIG
# ================================

# Timezone offset from UTC (IST = +5:30)
tz_offset_hours = 5.5

# Place – change if needed
latitude = 9.93     # Madurai approx (put your exact if you want)
longitude = 78.12   # Madurai approx


# Zodiac names
zodiac_signs = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrischika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

# Planet list
PLANETS = [
    swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER,
    swe.VENUS, swe.SATURN, swe.TRUE_NODE  # Rahu
]

# Nakshatras
NAKSHATRAS = [
    ("Ashwini", "Ketu"), ("Bharani", "Venus"), ("Krittika", "Sun"),
    ("Rohini", "Moon"), ("Mrigashira", "Mars"), ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"), ("Pushya", "Saturn"), ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"), ("Purva Phalguni", "Venus"), ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"), ("Chitra", "Mars"), ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"), ("Anuradha", "Saturn"), ("Jyeshtha", "Mercury"),
    ("Mula", "Ketu"), ("Purva Ashadha", "Venus"), ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"), ("Dhanishta", "Mars"), ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"), ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury"),
]


def get_nakshatra(longitude: float):
    """Given sidereal longitude 0–360°, return (nakshatra_name, pada, nakshatra_lord)."""
    nak_deg = 13.3333333333  # 13°20'
    total_nak = int(longitude // nak_deg)  # 0..26
    pada = int((longitude % nak_deg) // (nak_deg / 4)) + 1  # 1..4
    name, lord = NAKSHATRAS[total_nak]
    return name, pada, lord


def main():
    # -----------------------------------
    # 1) Setup Swiss Ephemeris: Lahiri
    # -----------------------------------
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)  # sidereal, Lahiri

    # -----------------------------------
    # 2) CURRENT LOCAL TIME (IST) → UTC
    # -----------------------------------
    # Always use current local time
    local_dt = datetime.datetime.now()

    # Convert local time to UTC using tz_offset_hours
    ut_dt = local_dt - datetime.timedelta(hours=tz_offset_hours)

    # Swiss Ephemeris: utc_to_jd to get JD(UT)
    jd_et, jd_ut = swe.utc_to_jd(
        ut_dt.year,
        ut_dt.month,
        ut_dt.day,
        ut_dt.hour,
        ut_dt.minute,
        ut_dt.second + ut_dt.microsecond / 1e6,
        1  # 1 = UT
    )

    print("===========================================")
    print(" VEDIC SIDEREAL (LAHIRI) CHART – NOW")
    print("===========================================")
    print(f"Local datetime : {local_dt}  (UTC+{tz_offset_hours})")
    print(f"UTC datetime   : {ut_dt}")
    print(f"JD UT          : {jd_ut:.6f}\n")

    # -----------------------------------
    # 3) Sidereal planets (Lahiri)
    # -----------------------------------
    planet_data = {}

    print("Planets (Sidereal Lahiri):\n")
    for pl in PLANETS:
        xx, flg = swe.calc_ut(jd_ut, pl, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)

        lon = xx[0]  # sidereal longitude
        rasi_index = int(lon // 30)
        deg_in_rasi = lon % 30

        rasi_name = zodiac_signs[rasi_index]
        pl_name = swe.get_planet_name(pl)
        if pl == swe.TRUE_NODE:
            pl_name = "Rahu"

        nak, pada, nak_lord = get_nakshatra(lon)

        print(f"{pl_name:7s}: {rasi_name:20s} {deg_in_rasi:05.2f}°"
              f" — {nak} (Pada {pada}, Lord: {nak_lord})")

        planet_data[pl_name] = {
            "longitude": lon,
            "raasi": rasi_name,
            "degree_in_raasi": deg_in_rasi,
            "nakshatra": nak,
            "nak_lord": nak_lord,
            "pada": pada,
        }

    # --- Ketu opposite Rahu ---
    rahu_lon = planet_data["Rahu"]["longitude"]
    ketu_lon = (rahu_lon + 180.0) % 360.0
    ketu_rasi_index = int(ketu_lon // 30)
    ketu_deg = ketu_lon % 30
    ketu_rasi = zodiac_signs[ketu_rasi_index]
    nak, pada, nak_lord = get_nakshatra(ketu_lon)

    print(f"Ketu   : {ketu_rasi:20s} {ketu_deg:05.2f}°"
          f" — {nak} (Pada {pada}, Lord: {nak_lord})\n")

    planet_data["Ketu"] = {
        "longitude": ketu_lon,
        "raasi": ketu_rasi,
        "degree_in_raasi": ketu_deg,
        "nakshatra": nak,
        "nak_lord": nak_lord,
        "pada": pada,
    }

    # -----------------------------------
    # 4) Sidereal Lagna & houses
    # -----------------------------------
    cusps, ascmc = swe.houses_ex(
        jd_ut,
        latitude,
        longitude,
        b'P',  # 'P' = Placidus; you can use 'E', 'W' etc. if you prefer
        flags=swe.FLG_SIDEREAL
    )

    asc_sid = ascmc[0]  # Ascendant already in sidereal longitude
    asc_index = int(asc_sid // 30)
    asc_deg_in_sign = asc_sid % 30
    asc_raasi = zodiac_signs[asc_index]

    print("Lagna & Houses (Sidereal Lahiri):\n")
    print(f"Lagna (Ascendant): {asc_raasi}, {asc_deg_in_sign:.2f}°\n")

    print("House Cusps (Sidereal):")
    for i, cusp_sid in enumerate(cusps, start=1):
        r_index = int(cusp_sid // 30)
        deg_in_sign = cusp_sid % 30
        r_name = zodiac_signs[r_index]
        print(f"House {i:2d}: {r_name}, {deg_in_sign:.2f}°")


if __name__ == "__main__":
    main()
