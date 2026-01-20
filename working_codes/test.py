
import datetime
import swisseph as swe

# ----------------------------
# BASIC ASTRO DICTS
# ----------------------------
rasi_dict = {
    1: "மேஷம் (Aries)", 2: "ரிஷபம் (Taurus)", 3: "மிதுனம் (Gemini)", 4: "கடகம் (Cancer)",
    5: "சிம்மம் (Leo)", 6: "கன்னி (Virgo)", 7: "துலாம் (Libra)", 8: "விருச்சிகம் (Scorpio)",
    9: "தனுசு (Sagittarius)", 10: "மகரம் (Capricorn)", 11: "கும்பம் (Aquarius)", 12: "மீனம் (Pisces)"
}

rasi_lords = {
    1: "செவ்வாய்", 2: "சுக்கிரன்", 3: "புதன்", 4: "சந்திரன்",
    5: "சூரியன்", 6: "புதன்", 7: "சுக்கிரன்", 8: "செவ்வாய்",
    9: "குரு", 10: "சனி", 11: "சனி", 12: "குரு"
}

tamil_months = {
    1: "சித்திரை", 2: "வைகாசி", 3: "ஆனி", 4: "ஆடி", 5: "ஆவணி", 6: "புரட்டாசி",
    7: "ஐப்பசி", 8: "கார்த்திகை", 9: "மார்கழி", 10: "தை", 11: "மாசி", 12: "பங்குனி"
}

tz_offset_hours = 5.5       # IST
latitude = 9.93             # Madurai approx – change if needed
longitude = 78.12



############################# ARUDAM - CALCULAION #################################
def get_arudam(dt: datetime.datetime):
    """
    Arudam based on minute:
    00–04 → 1, 05–09 → 2, ..., 55–59 → 12
    """
    arudam_no = (dt.minute // 5) + 1
    arudam_rasi = rasi_dict[arudam_no]

    return {
        "arudam_no": arudam_no,
        "arudam_rasi": arudam_rasi
    }
# ----------------------------
# TAMIL MONTH (APPROX BOUNDARIES)
# ----------------------------
def get_tamil_month_no_from_gregorian(dt: datetime.datetime) -> int:
    m, d = dt.month, dt.day
    if   (m == 4 and d >= 14) or (m == 5 and d <= 14):  return 1
    elif (m == 5 and d >= 15) or (m == 6 and d <= 14):  return 2
    elif (m == 6 and d >= 15) or (m == 7 and d <= 16):  return 3
    elif (m == 7 and d >= 17) or (m == 8 and d <= 16):  return 4
    elif (m == 8 and d >= 17) or (m == 9 and d <= 16):  return 5
    elif (m == 9 and d >= 17) or (m == 10 and d <= 16): return 6
    elif (m == 10 and d >= 17) or (m == 11 and d <= 15): return 7
    elif (m == 11 and d >= 16) or (m == 12 and d <= 15): return 8
    elif (m == 12 and d >= 16) or (m == 1 and d <= 13):  return 9
    elif (m == 1 and d >= 14) or (m == 2 and d <= 12):   return 10
    elif (m == 2 and d >= 13) or (m == 3 and d <= 13):   return 11
    else:                                                return 12  # (m==3,d>=14) or (m==4,d<=13)


############################# FIRST RAASI - CALCULAION #################################
def get_first_rasi_for_tamil_month(tamil_month_no: int) -> int:
    return tamil_month_no if 1 <= tamil_month_no <= 12 else 1


# ----------------------------
# SUNRISE / SUNSET
# ----------------------------
def get_sunrise_sunset(local_dt, tz_offset_hours, latitude, longitude):
    y, m, d = local_dt.year, local_dt.month, local_dt.day
    ut_midnight = datetime.datetime(y, m, d, 0, 0, 0) - datetime.timedelta(hours=tz_offset_hours)

    _, jd_ut = swe.utc_to_jd(
        ut_midnight.year, ut_midnight.month, ut_midnight.day,
        ut_midnight.hour, ut_midnight.minute, ut_midnight.second, 1
    )

    geopos = [longitude, latitude, 0.0]

    sr = swe.rise_trans(jd_ut, swe.SUN, rsmi=swe.CALC_RISE, geopos=geopos, atpress=1013.25, attemp=15)[1][0]
    ss = swe.rise_trans(jd_ut, swe.SUN, rsmi=swe.CALC_SET,  geopos=geopos, atpress=1013.25, attemp=15)[1][0]

    sy, smo, sd, sh, smin, ssec = swe.jdut1_to_utc(sr)
    ey, emo, ed, eh, emin, esec = swe.jdut1_to_utc(ss)

    def to_dt(y, mo, d, h, mi, secf):
        sec = int(secf)
        micro = int(round((secf - sec) * 1_000_000))
        return datetime.datetime(int(y), int(mo), int(d), int(h), int(mi), sec, micro)

    sunrise_local = to_dt(sy, smo, sd, sh, smin, ssec) + datetime.timedelta(hours=tz_offset_hours)
    sunset_local  = to_dt(ey, emo, ed, eh, emin, esec) + datetime.timedelta(hours=tz_offset_hours)
    return sunrise_local, sunset_local

def calculate_one_uthayam(sunrise_local, sunset_local): # WORKING
    total_min = int((sunset_local - sunrise_local).total_seconds() / 60)
    one_uthayam_min = int(round(total_min / 12))
    return one_uthayam_min

local_dt = datetime.datetime.now()
# Step 1: Get sunrise & sunset
sr, ss = get_sunrise_sunset(local_dt, tz_offset_hours, latitude, longitude)
# (Optional) reduce 30 seconds
sr -= datetime.timedelta(seconds=36)
ss -= datetime.timedelta(seconds=36)

# Step 2: Get one uthayam minutes
one_uthayam_min = calculate_one_uthayam(sr, ss)

# ----------------------------
# YOUR JAMAKOL RULE PLACEHOLDER
# ----------------------------
def get_tamil_date_number(local_dt: datetime.datetime) -> int:
    return local_dt.day  # replace later with exact tamil day if needed

def calculate_first_uthaya_mudivu(sunrise_local, sunset_local, local_dt):
    tamil_date = get_tamil_date_number(local_dt)
    sun_date = tamil_date * 2

    day_time = sunset_local -sunrise_local

    # suriyam_irupu = one_uthayam_min - multiplied
    # first_end = sunrise_local + datetime.timedelta(minutes=suriyam_irupu)
    # return first_end


# ----------------------------
# UTHAYAM TABLE
# ----------------------------
def generate_uthayams(
    sunrise_local,
    first_uthaya_mudivuu,
    one_uthayam_minutes,
    first_rasi_no,
    count=24
):
    uthayams = []

    start = sunrise_local      # ✅ correct start
    end = first_uthaya_mudivuu  # ✅ correct first mudivu

    for i in range(count):
        rasi_no = ((first_rasi_no - 1 + i) % 12) + 1

        uthayams.append({
            "uthayam_no": i + 1,
            "rasi_no": rasi_no,
            "rasi_name": rasi_dict[rasi_no],
            "rasi_lord": rasi_lords[rasi_no],
            "start": start,
            "end": end
        })

        start = end
        end = end + datetime.timedelta(minutes=one_uthayam_minutes)

    return uthayams

# ----------------------------
# SINGLE PIPELINE
# ----------------------------
def run_prasna_pipeline(
    tz_offset_hours=5.5,
    latitude=9.93,
    longitude=78.12,
    local_dt=None,
    uthayam_count=None,          # if None → auto-calc
    reduce_seconds=30,           # reduce sunrise/sunset by this many seconds
    do_print=True
):
    local_dt = local_dt or datetime.datetime.now()

    # Arudam (minute based)
    arudam_info = get_arudam(local_dt)

    # Tamil month + first rasi
    tamil_month_no = get_tamil_month_no_from_gregorian(local_dt)
    first_rasi_no = get_first_rasi_for_tamil_month(tamil_month_no)

    # Sunrise / Sunset
    sr, ss = get_sunrise_sunset(local_dt, tz_offset_hours, latitude, longitude)

    # Optional: reduce seconds
    if reduce_seconds and reduce_seconds > 0:
        offset = datetime.timedelta(seconds=reduce_seconds)
        sr -= offset
        ss -= offset

    # Total daylight + one uthayam minutes
    total_min = int((ss - sr).total_seconds() / 60)
    one_uthayam_min = calculate_one_uthayam(sr, ss)



    # First uthaya mudivu (your rule)
    #first_uthaya_mudivu = calculate_first_uthaya_mudivu(sr, local_dt)
    first_uthaya_mudivuu = calculate_first_uthaya_mudivuu(sr, ss,local_dt, 16)
    # Auto-calc uthayam_count to fit sunrise→sunset (recommended)
    if uthayam_count is None:
        # number of full uthayam blocks that fit in the daylight duration
        uthayam_count = max(1, total_min // one_uthayam_min)

    # Generate uthayams
    uthayams = generate_uthayams(sunrise_local=sr,
        first_uthaya_mudivu=first_uthaya_mudivuu,
        one_uthayam_minutes=one_uthayam_min,
        first_rasi_no=first_rasi_no,
        count=uthayam_count)

    # Print (optional)
    if do_print:
        print("local_dt            :", local_dt.strftime("%Y-%m-%d %H:%M:%S"))
        print("Sunrise             :", sr.strftime("%Y-%m-%d %H:%M:%S"))
        print("Sunset              :", ss.strftime("%Y-%m-%d %H:%M:%S"))
        print("Total daylight (min):", total_min)
        print("One uthayam (min)   :", one_uthayam_min)
        print("Tamil month         :", tamil_month_no, "-", tamil_months[tamil_month_no])
        print("First uthaya rasi   :", rasi_dict[first_rasi_no])
        #print("First uthaya mudivu :", first_uthaya_mudivu.strftime("%Y-%m-%d %H:%M:%S"))
        print("Uthayam count       :", uthayam_count)
        print("Arudam number       :", arudam_info["arudam_no"])
        print("Arudam rasi1         :", arudam_info["arudam_rasi"])


    return {
        "local_dt": local_dt,
        "tamil_month_no": tamil_month_no,
        "tamil_month_name": tamil_months[tamil_month_no],
        "sunrise": sr,
        "sunset": ss,
        "total_daylight_min": total_min,
        "one_uthayam_min": one_uthayam_min,
        #"first_uthaya_mudivu": first_uthaya_mudivu,
        "first_rasi_no": first_rasi_no,
        "first_rasi_name": rasi_dict[first_rasi_no],
        "uthayam_count": uthayam_count,
        "uthayams": uthayams,
        "arudam_no": arudam_info["arudam_no"],
        "arudam_rasi": arudam_info["arudam_rasi"]
    }


# ----------------------------
# RUN
# ----------------------------
out = run_prasna_pipeline()
uthayams = out["uthayams"]

print(uthayams)


