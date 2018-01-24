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

DAY_OF_WEEK_CHOICES = (
    (WEEKDAY, 'Weekday'),
    (WEEKEND, 'Weekend'),
)

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
