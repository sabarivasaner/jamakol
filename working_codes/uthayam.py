
import datetime
import swisseph as swe
dt = datetime.datetime.now()
arudam_no = (dt.minute // 5) + 1

    # Degree calculation
arudam_start_degree = (arudam_no - 1) * 30
arudam_end_degree = arudam_no * 30
minute_in_arudam = dt.minute % 5
degree_progress =  minute_in_arudam * 6
current_degree = arudam_start_degree + minute_in_arudam
print(arudam_start_degree,arudam_end_degree,current_degree,degree_progress)