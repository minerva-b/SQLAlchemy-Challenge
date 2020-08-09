# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<b>Welcome to the Climate API</b></br>"
        f"Available Routes:</b></br>"
        f"<li>List of Precipitation: /api/v1.0/precipitation<br/>"
        f"<li>List of Stations: /api/v1.0/stations<br/>"
        f"<li>List of Temperature Observation Data (TOBS): /api/v1.0/tobs<br/>"
        f"<li>Search for data by entering start date (format 'yyyy-mm-dd'): /api/v1.0/<start><br/>"
        f"<li>Search for data by entering start and end date (format 'yyyy-mm-dd'): /api/v1.0/yyyy-mm-dd<start>/yyyy-mm-dd<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation"""
    # Query all dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    """Return a JSON dict of all dates and precipitation"""
    # Convert the query results to a dictionary using 'date' as the key and 'prcp' as the value
    # Create a dictionary from the row data and append to a list of date_prcp_list
    date_prcp_list = []

    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict['date'] = date
        date_prcp_dict['prcp'] = precipitation
        date_prcp_list.append(date_prcp_dict)

    # Close each session to avoid running errors
    session.close()

    return jsonify(date_prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from dataset"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    # Close each session to avoid running errors
    session.close()

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations (TOBS) for the last year of data"""
    # Query the dates and temperature observations (tobs) of the most active station for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= dt.date(2016, 8, 23)).all()

    # Close each session to avoid running errors
    session.close()

    return jsonify(results)


@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start"""
    # Query the dates and tobs for given start date
    results = session.query(Measurement.date >= start).filter(Measurement.tobs).all()

    # Create a list to store date and temperature info
    temp_by_start_date = []
    for result in results:
        temp_by_start_date.append(result[1])

    # Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    TMIN = min(temp_by_start_date)
    TAVG = (sum(temp_by_start_date) / len(temp_by_start_date))
    TMAX = max(temp_by_start_date)

    # Close each session to avoid running errors
    session.close()

    return jsonify(
        f"Maximum Temperature: {TMAX}<br/>"
        f"Minimum Temperature: {TMIN}<br/>"
        f"Average Temperature: {round(TAVG, 2)}"
    )

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range"""
    # Query the dates and tobs for given start and end dates
    results = session.query(Measurement.date >= start).filter(Measurement.date <= end).filter(Measurement.tobs).all()

    # Create a list to store dates and temperature info
    temp_by_start_end_dates = []
    for result in results:
        temp_by_start_end_dates.append(result[2])

    # Calculate the TMIN, TAVG, and TMAX for dates between the start and end dates inclusive
    TMIN = min(temp_by_start_end_dates)
    TAVG = (sum(temp_by_start_date) / len(temp_by_start_end_dates))
    TMAX = max(temp_by_start_end_dates)

    # Close each session to avoid running errors
    session.close()

    return jsonify(
        f"Maximum Temperature: {TMAX}<br/>"
        f"Minimum Temperature: {TMIN}<br/>"
        f"Average Temperature: {round(TAVG, 2)}"
    )

# Need to run app.py
if __name__ == '__main__':
    app.run(debug=True)