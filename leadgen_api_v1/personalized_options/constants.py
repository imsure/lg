PROB_THRESHOLD = 25.0

HOME = 'H'
WORK = 'W'
SCHOOL = 'SC'
SHOPPING = 'SH'
MAINTENANCE = 'M'
RECREATIONAL = 'R'
PICKUP_DROPOFF = 'PD'

PURPOSE_CHOICES = (
    (HOME, 'Home'),
    (WORK, 'Work'),
    (SCHOOL, 'School'),
    (SHOPPING, 'Shopping'),
    (MAINTENANCE, 'Maintenance'),
    (RECREATIONAL, 'Recreational'),
    (PICKUP_DROPOFF, 'Pickup/DropOff'),
)

WEEKDAY = 'WD'
WEEKEND = 'WE'
MONDAY = 'MO'
TUESDAY = 'TU'
WEDNESDAY = 'WE'
THURSDAY = 'TH'
FRIDAY = 'FR'
SATURDAY = 'SA'
SUNDAY = 'SU'

DAY_OF_WEEK_CHOICES = (
    (WEEKDAY, 'Weekday'),
    (WEEKEND, 'Weekend'),
    (MONDAY, 'Monday'),
    (TUESDAY, 'Tuesday'),
    (WEDNESDAY, 'Wednesday'),
    (THURSDAY, 'Thursday'),
    (FRIDAY, 'Friday'),
    (SATURDAY, 'Saturday'),
    (SUNDAY, 'Sunday'),
)

DAY_OF_WEEK_VALID_SET1 = {MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY}
DAY_OF_WEEK_VALID_SET2 = {MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, WEEKEND}
DAY_OF_WEEK_VALID_SET3 = {WEEKDAY, SATURDAY, SUNDAY}
DAY_OF_WEEK_VALID_SET4 = {WEEKDAY, WEEKEND}

DRIVING = 'DR'
PUBLIC_TRANSIT = 'PT'
WALKING = 'WK'
BIKING = 'BK'
UBERX = 'UX'
UBERPOOL = 'UP'

MODE_CHOICES = (
    (DRIVING, 'Driving'),
    (PUBLIC_TRANSIT, 'Public Transit'),
    (WALKING, 'Walking'),
    (BIKING, 'Biking'),
    (UBERX, 'UberX'),
    (UBERPOOL, 'UberPool'),
)

America_Phoenix = 'AP'  # Tucson
America_Chicago = 'AC'  # Austin
America_Denver = 'AD'   # El Paso

TZ_CHOICES = (
    (America_Phoenix, 'America/Phoenix'),
    (America_Chicago, 'America/Chicago'),
    (America_Denver, 'America/Denver'),
)

TZ_MAP = {
    'America/Phoenix': America_Phoenix,
    'America/Chicago': America_Chicago,
    'America/Denver': America_Denver,
}
