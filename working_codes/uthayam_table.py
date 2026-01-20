# notes: Uthayam table is working. need to finetune the kavipu and arudam table.
#todo: uthyam calculation is easy. already almost ready
#todo: kavipu - to work
#todo: uthayam calculation. little lengthy. need to reduce the lines and make it compact.
#todo: finding all the degrees in same function.
#todo: plotting all with degree.
#todo: to maintain the jamakol name as it is.
#todo: kiraka palam
#todo: kathir
#todo: anthi kanitham
#todo: kiraka serkai
#todo:

import swisseph as swe
import datetime

local_dt = datetime.datetime.now()

# ================================
# BASIC ASTRO DICTS
# ================================

rasi_dict = {
    1: "மேஷம் (Aries)",
    2: "ரிஷபம் (Taurus)",
    3: "மிதுனம் (Gemini)",
    4: "கடகம் (Cancer)",
    5: "சிம்மம் (Leo)",
    6: "கன்னி (Virgo)",
    7: "துலாம் (Libra)",
    8: "விருச்சிகம் (Scorpio)",
    9: "தனுசு (Sagittarius)",
    10: "மகரம் (Capricorn)",
    11: "கும்பம் (Aquarius)",
    12: "மீனம் (Pisces)"
}

# Rasi lords (Vedic standard)
rasi_lords = {
    1: "செவ்வாய்",    # Mesha
    2: "சுக்கிரன்",   # Vrishabha
    3: "புதன்",      # Mithuna
    4: "சந்திரன்",   # Karka
    5: "சூரியன்",    # Simha
    6: "புதன்",      # Kanya
    7: "சுக்கிரன்",   # Tula
    8: "செவ்வாய்",    # Vrischika
    9: "குரு",       # Dhanu
    10: "சனி",       # Makara
    11: "சனி",       # Kumbha
    12: "குரு"       # Meena
}

tamil_months = {
    1: "சித்திரை",
    2: "வைகாசி",
    3: "ஆனி",
    4: "ஆடி",
    5: "ஆவணி",
    6: "புரட்டாசி",
    7: "ஐப்பசி",
    8: "கார்த்திகை",
    9: "மார்கழி",
    10: "தை",
    11: "மாசி",
    12: "பங்குனி"
}
def get_sunrise_sunset(local_dt, tz_offset_hours, latitude, longitude):
    """
    Returns (sunrise_local, sunset_local) datetime objects
    for the given date and location.
    """

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Calculating sunrise & sunset...")

    year = local_dt.year
    month = local_dt.month
    day = local_dt.day

    # Local midnight → UTC midnight
    ut_midnight = datetime.datetime(year, month, day, 0, 0, 0) - datetime.timedelta(hours=tz_offset_hours)

    # Convert UTC → JD
    jd_et, jd_ut = swe.utc_to_jd(
        ut_midnight.year,
        ut_midnight.month,
        ut_midnight.day,
        ut_midnight.hour,
        ut_midnight.minute,
        ut_midnight.second,
        1   # 1 = UT
    )

    # Geographical position [longitude, latitude, elevation_m]
    geopos = [longitude, latitude, 0.0]

    # --- Sunrise (top of disc, with refraction) ---
    sr_flag = swe.CALC_RISE
    sr_res = swe.rise_trans(
        jd_ut,
        swe.SUN,
        rsmi=sr_flag,
        geopos=geopos,
        atpress=1013.25,
        attemp=15
    )

    # --- Sunset ---
    ss_flag = swe.CALC_SET
    ss_res = swe.rise_trans(
        jd_ut,
        swe.SUN,
        rsmi=ss_flag,
        geopos=geopos,
        atpress=1013.25,
        attemp=15
    )

    # Convert JD → UTC datetime parts (year, month, day, hour, min, sec_float)
    sunrise_utc = swe.jdut1_to_utc(sr_res[1][0])
    sunset_utc = swe.jdut1_to_utc(ss_res[1][0])

    # Unpack & convert to datetime, handling float seconds
    sy, smo, sd, sh, smin, ssec = sunrise_utc
    sunrise_sec = int(ssec)
    sunrise_micro = int(round((ssec - sunrise_sec) * 1_000_000))

    sunrise_dt_utc = datetime.datetime(
        int(sy), int(smo), int(sd),
        int(sh), int(smin), sunrise_sec,
        sunrise_micro
    )

    ey, emo, ed, eh, emin, esec = sunset_utc
    sunset_sec = int(esec)
    sunset_micro = int(round((esec - sunset_sec) * 1_000_000))

    sunset_dt_utc = datetime.datetime(
        int(ey), int(emo), int(ed),
        int(eh), int(emin), sunset_sec,
        sunset_micro
    )

    # UTC → Local
    sunrise_local = sunrise_dt_utc + datetime.timedelta(hours=tz_offset_hours)
    sunset_local  = sunset_dt_utc  + datetime.timedelta(hours=tz_offset_hours)

    return sunrise_local, sunset_local

def get_tamil_month_no_from_gregorian(dt: datetime.datetime) -> int:
    """
    Return Tamil month number (1–12) for given Gregorian date.
    Solar month boundaries (approx, standard panchang style):

      1  சித்திரை    : Apr 14 – May 14
      2  வைகாசி      : May 15 – Jun 14
      3  ஆனி         : Jun 15 – Jul 16
      4  ஆடி         : Jul 17 – Aug 16
      5  ஆவணி       : Aug 17 – Sep 16
      6  புரட்டாசி    : Sep 17 – Oct 16
      7  ஐப்பசி      : Oct 17 – Nov 15
      8  கார்த்திகை  : Nov 16 – Dec 15
      9  மார்கழி     : Dec 16 – Jan 13
      10 தை          : Jan 14 – Feb 12
      11 மாசி        : Feb 13 – Mar 13
      12 பங்குனி     : Mar 14 – Apr 13
    """
    y, m, d = dt.year, dt.month, dt.day

    if   (m == 4 and d >= 14) or (m == 5 and d <= 14):
        return 1   # சித்திரை
    elif (m == 5 and d >= 15) or (m == 6 and d <= 14):
        return 2   # வைகாசி
    elif (m == 6 and d >= 15) or (m == 7 and d <= 16):
        return 3   # ஆனி
    elif (m == 7 and d >= 17) or (m == 8 and d <= 16):
        return 4   # ஆடி
    elif (m == 8 and d >= 17) or (m == 9 and d <= 16):
        return 5   # ஆவணி
    elif (m == 9 and d >= 17) or (m == 10 and d <= 16):
        return 6   # புரட்டாசி
    elif (m == 10 and d >= 17) or (m == 11 and d <= 15):
        return 7   # ஐப்பசி
    elif (m == 11 and d >= 16) or (m == 12 and d <= 15):
        return 8   # கார்த்திகை
    elif (m == 12 and d >= 16) or (m == 1 and d <= 13):
        return 9   # மார்கழி
    elif (m == 1 and d >= 14) or (m == 2 and d <= 12):
        return 10  # தை
    elif (m == 2 and d >= 13) or (m == 3 and d <= 13):
        return 11  # மாசி
    elif (m == 3 and d >= 14) or (m == 4 and d <= 13):
        return 12  # பங்குனி

    # fallback
    return 1

def get_first_rasi_for_tamil_month(tamil_month_no: int) -> int:
    """
    Your rule:
    Always the first uthayam will be the rasi of the current Tamil month number.
    So we map 1→1, 2→2, ..., 12→12.
    """
    if 1 <= tamil_month_no <= 12:
        return tamil_month_no
    return 1

def first_uthaya_rasi():
    # Today (or any Prasna date)

    # Tamil month no from date
    local_dt = datetime.datetime.now()
    tamil_month_no = get_tamil_month_no_from_gregorian(local_dt)
    print(tamil_month_no)
    first_rasi_no = get_first_rasi_for_tamil_month(tamil_month_no)
    print("First uthaya rasi    :", rasi_dict[first_rasi_no])
first_uthaya_rasi()

def get_arudam():
    dt = datetime.datetime.now()
    arudam = (dt.minute // 5) + 1
    print("aruda number:", arudam)
    print("Aruda rasi :", rasi_dict[arudam])
get_arudam()

# ================================
# TAMIL MONTH CALC (SOLAR)
# ================================



def get_first_rasi_for_tamil_month(tamil_month_no: int) -> int:
    """
    Your rule:
    Always the first uthayam will be the rasi of the current Tamil month number.
    So we map 1→1, 2→2, ..., 12→12.
    """
    if 1 <= tamil_month_no <= 12:
        return tamil_month_no
    return 1

# ================================
# SUNRISE / SUNSET
# ================================

def get_sunrise_sunset(local_dt, tz_offset_hours, latitude, longitude):
    """
    Returns (sunrise_local, sunset_local) datetime objects
    for the given date and location.
    """

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Calculating sunrise & sunset...")

    year = local_dt.year
    month = local_dt.month
    day = local_dt.day

    # Local midnight → UTC midnight
    ut_midnight = datetime.datetime(year, month, day, 0, 0, 0) - datetime.timedelta(hours=tz_offset_hours)

    # Convert UTC → JD
    jd_et, jd_ut = swe.utc_to_jd(
        ut_midnight.year,
        ut_midnight.month,
        ut_midnight.day,
        ut_midnight.hour,
        ut_midnight.minute,
        ut_midnight.second,
        1   # 1 = UT
    )

    # Geographical position [longitude, latitude, elevation_m]
    geopos = [longitude, latitude, 0.0]

    # --- Sunrise (top of disc, with refraction) ---
    sr_flag = swe.CALC_RISE
    sr_res = swe.rise_trans(
        jd_ut,
        swe.SUN,
        rsmi=sr_flag,
        geopos=geopos,
        atpress=1013.25,
        attemp=15
    )

    # --- Sunset ---
    ss_flag = swe.CALC_SET
    ss_res = swe.rise_trans(
        jd_ut,
        swe.SUN,
        rsmi=ss_flag,
        geopos=geopos,
        atpress=1013.25,
        attemp=15
    )

    # Convert JD → UTC datetime parts (year, month, day, hour, min, sec_float)
    sunrise_utc = swe.jdut1_to_utc(sr_res[1][0])
    sunset_utc = swe.jdut1_to_utc(ss_res[1][0])

    # Unpack & convert to datetime, handling float seconds
    sy, smo, sd, sh, smin, ssec = sunrise_utc
    sunrise_sec = int(ssec)
    sunrise_micro = int(round((ssec - sunrise_sec) * 1_000_000))

    sunrise_dt_utc = datetime.datetime(
        int(sy), int(smo), int(sd),
        int(sh), int(smin), sunrise_sec,
        sunrise_micro
    )

    ey, emo, ed, eh, emin, esec = sunset_utc
    sunset_sec = int(esec)
    sunset_micro = int(round((esec - sunset_sec) * 1_000_000))

    sunset_dt_utc = datetime.datetime(
        int(ey), int(emo), int(ed),
        int(eh), int(emin), sunset_sec,
        sunset_micro
    )

    # UTC → Local
    sunrise_local = sunrise_dt_utc + datetime.timedelta(hours=tz_offset_hours)
    sunset_local  = sunset_dt_utc  + datetime.timedelta(hours=tz_offset_hours)

    return sunrise_local, sunset_local

# ================================
# ONE UTHAYAM + JAMAKOL LOGIC
# ================================

def calculate_one_uthayam(sunrise_local, sunset_local):
    """
    Day length / 12, rounded to nearest minute.
    Returns (total_day_minutes_int, one_uthayam_minutes_int)
    """
    day_length = sunset_local - sunrise_local
    total_minutes = day_length.total_seconds() / 60
    total_minutes_rounded = int(round(total_minutes))
    one_uthayam123 = int(round(total_minutes_rounded / 12))
    return one_uthayam123

def get_tamil_date_number(local_dt: datetime.datetime) -> int:
    """
    Placeholder: using Gregorian day as Tamil day.
    Replace later with real Tamil date if needed.
    """
    return local_dt.day

def calculate_first_uthaya_mudivu(sunrise_local, one_uthayam123, local_dt):
    """
    Your rule:
      tamil_date = date number
      multiplied = tamil_date * 2
      to_subtract = one_uthayam - multiplied
      balance = one_uthayam - to_subtract (== multiplied)
      first_uthaya_mudivu = sunrise + balance minutes
    """
    tamil_date = get_tamil_date_number(local_dt)
    multiplied = tamil_date * 2
    to_subtract123 = one_uthayam123 - multiplied
    balance123 = one_uthayam123 - to_subtract123  # effectively tamil_date * 2

    first_uthaya_mudivu = sunrise_local + datetime.timedelta(minutes=balance123)

    debug = {
        "tamil_date": tamil_date,
        "multiplied": multiplied,
        "to_subtract123": to_subtract123,
        "balance123": balance123
    }

    return first_uthaya_mudivu, debug

# ================================
# UTHAYAM TABLE GENERATOR
# ================================

def generate_uthayams(first_uthaya_mudivu, one_uthayam_minutes, first_rasi_no):
    """
    Generate 12 uthayams:
      - first uthayam rasi = first_rasi_no
      - each uthayam length = one_uthayam_minutes
      - returns list of dicts
    """
    uthayams = []
    current_end = first_uthaya_mudivu
    current_start = current_end - datetime.timedelta(minutes=one_uthayam_minutes)

    for i in range(26):
        rasi_index = ((first_rasi_no - 1 + i) % 12) + 1
        rasi_name = rasi_dict[rasi_index]
        graha_lord = rasi_lords[rasi_index]

        uthayams.append({
            "uthayam_no": i + 1,
            "rasi_no": rasi_index,
            "rasi_name": rasi_name,
            "rasi_lord": graha_lord,
            "start": current_start,
            "end": current_end
        })

        current_start = current_end
        current_end = current_end + datetime.timedelta(minutes=one_uthayam_minutes)

    return uthayams

def print_jamakol_table(uthayams, now_local=None):
    """
    Print a Jamakol-style table.
    Marks current uthayam with '*', if now_local is given.
    """
    print("\n================ JAMAKோL PRASNம – UTHAYAM TABLE ================\n")
    print(f"{'No':>2}  {'Rasi':<20} {'Lord':<8} {'Start':<8}  {'End':<8}  {'Now?'}")
    print("-" * 70)
    for u in uthayams:
        mark = ""
        if now_local is not None and u["start"] <= now_local < u["end"]:
            mark = "*"
        print(
            f"{u['uthayam_no']:2d}  "
            f"{u['rasi_name']:<20} "
            f"{u['rasi_lord']:<8} "
            f"{u['start'].strftime('%H:%M'):>5}   "
            f"{u['end'].strftime('%H:%M'):>5}   "
            f"{mark}"
        )
    print("\n* = current running uthayam (if 'now' passed)\n")



def find_uthayams_for_rasi(uthayams, rasi_no):
    """
    Given the uthayams list and a rasi number (1–12),
    return all uthayams where this rasi is active.
    (In your current model, each uthayam has exactly one rasi.)
    """
    return [u for u in uthayams if u["rasi_no"] == rasi_no]

def print_arudam_table(uthayams, arudam_rasi_no):
    """
    Prints a table showing which uthayam(s) correspond to Arudam rasi.
    You decide how to calculate arudam_rasi_no before calling this.
    """
    matches = find_uthayams_for_rasi(uthayams, arudam_rasi_no)

    print("\n================ ARUDAM TABLE ================\n")
    print(f"Arudam Rasi : {rasi_dict[arudam_rasi_no]}")
    print("----------------------------------------------")
    print(f"{'No':>2}  {'Rasi':<20} {'Lord':<8} {'Start':<8}  {'End':<8}")
    print("----------------------------------------------")

    for u in matches:
        print(
            f"{u['uthayam_no']:2d}  "
            f"{u['rasi_name']:<20} "
            f"{u['rasi_lord']:<8} "
            f"{u['start'].strftime('%H:%M'):>5}   "
            f"{u['end'].strftime('%H:%M'):>5}"
        )

    if not matches:
        print("No uthayam found with this Arudam rasi (check input).")

    print("----------------------------------------------\n")

def print_kavipu_table(uthayams, kavipu_rasi_no):
    """
    Prints a table showing which uthayam(s) correspond to Kavipu rasi.
    """
    matches = find_uthayams_for_rasi(uthayams, kavipu_rasi_no)

    print("\n================ KAVIPU TABLE ================\n")
    print(f"Kavipu Rasi : {rasi_dict[kavipu_rasi_no]}")
    print("----------------------------------------------")
    print(f"{'No':>2}  {'Rasi':<20} {'Lord':<8} {'Start':<8}  {'End':<8}")
    print("----------------------------------------------")

    for u in matches:
        print(
            f"{u['uthayam_no']:2d}  "
            f"{u['rasi_name']:<20} "
            f"{u['rasi_lord']:<8} "
            f"{u['start'].strftime('%H:%M'):>5}   "
            f"{u['end'].strftime('%H:%M'):>5}"
        )

    if not matches:
        print("No uthayam found with this Kavipu rasi (check input).")

    print("----------------------------------------------\n")


# ================================
# MAIN – DEMO JAMAKOL TABLE
# ================================

if __name__ == "__main__":
    # Location & timezone
    tz_offset_hours = 5.5       # IST
    latitude = 9.93             # Madurai approx – change if needed
    longitude = 78.12

    # Today (or any Prasna date)
    local_dt = datetime.datetime.now()

    # Tamil month no from date
    tamil_month_no = get_tamil_month_no_from_gregorian(local_dt)

    # 1) Sunrise & sunset
    sr, ss = get_sunrise_sunset(local_dt, tz_offset_hours, latitude, longitude)
    print("Sunrise:", sr.strftime("%Y-%m-%d %H:%M:%S"))
    print("Sunset :", ss.strftime("%Y-%m-%d %H:%M:%S"))

    # 2) Day length / one uthayam
    total_min, one_uthayam123 = calculate_one_uthayam(sr, ss)
    print("\nTotal daylight (min):", total_min)
    print("one_uthayam123 (min):", one_uthayam123)

    # 3) First uthaya mudivu (your Jamakol rule)
    first_uthaya_mudivu, debug_vals = calculate_first_uthaya_mudivu(sr, one_uthayam123, local_dt)
    print("\nTamil date today     :", debug_vals["tamil_date"])
    print("Tamil date × 2       :", debug_vals["multiplied"])
    print("to_subtract123       :", debug_vals["to_subtract123"])
    print("balance123 (minutes) :", debug_vals["balance123"])
    print("first_uthaya_mudivu  :", first_uthaya_mudivu.strftime("%Y-%m-%d %H:%M:%S"))

    # 4) First rasi = rasi of Tamil month
    first_rasi_no = get_first_rasi_for_tamil_month(tamil_month_no)
    print("\nTamil month no       :", tamil_month_no, "-", tamil_months.get(tamil_month_no, ""))
    print("First uthaya rasi    :", rasi_dict[first_rasi_no])

    # 5) Generate and print Jamakol table
    uthayams = generate_uthayams(first_uthaya_mudivu, one_uthayam123, first_rasi_no)
    print_jamakol_table(uthayams, now_local=local_dt)


    arudam_rasi_no = ((first_rasi_no - 1 + 6) % 12) + 1  # 7th from lagna
    kavipu_rasi_no = ((first_rasi_no - 1 + 8) % 12) + 1  # 9th from lagna (just example)

    print_arudam_table(uthayams, arudam_rasi_no)
    print_kavipu_table(uthayams, kavipu_rasi_no)