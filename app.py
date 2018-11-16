# SKYFIELD SETUP
from skyfield import api
ts = api.load.timescale()
e = api.load('de421.bsp')
from skyfield import almanac

# FLASK SETUP
from flask import Flask, Response
app = Flask(__name__)

# OTHER MODULE SETUP
import emoji
from icalendar import Calendar, Event
from datetime import date, timedelta

# CONSTANTS
MOON_PHASES = [
    emoji.emojize(":new_moon: New Moon"),
    emoji.emojize(":first_quarter_moon: First Quarter Moon"),
    emoji.emojize(":full_moon: Full Moon"),
    emoji.emojize(":last_quarter_moon: Last Quarter Moon")
]
CAL_NAME = "Lunar Phases"
CAL_COLOR = "#003153"

# MOON PHASE FUNCTION
def moon_phase_list(t0, t1):
    t, p = almanac.find_discrete(t0, t1, almanac.moon_phases(e))

    l = []
    for i in range(0, len(t)):
        l.append({
            't': t[i].utc_datetime(),
            'p': p[i]
        })

    return l

@app.route("/")
def cal():
    # define time variables
    today = date.today()
    year = timedelta(days=365)

    # define time interval
    t0 = ts.utc(today - 2 * year)
    t1 = ts.utc(today + 2 * year)

    # create calendar object
    cal = Calendar()
    cal.add('dtstart', t0.utc_datetime().date())
    cal.add('name', CAL_NAME)
    cal.add('x-wr-calname', CAL_NAME)
    cal.add('x-apple-calendar-color', CAL_COLOR)

    # create event objects
    for i in moon_phase_list(t0, t1):
        event = Event()
        event.add('dtstart', i.get('t').date()) # using a date object for dtstart infers an all day event
        event.add('summary', MOON_PHASES[i.get('p')])
        cal.add_component(event)

    # generate response
    return Response(cal.to_ical(), mimetype="text/calendar")
