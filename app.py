import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data"""
    # Query the last 12 months of precipitation data
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>dt.date(2016,8,24)).all()

    # create dictionary
    prcp_dict = {date: prcp for date, prcp in precipitation}
    
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return stations data"""
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return temperature observations"""

    # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date>dt.date(2016,8,24)).all()

    # Create List
    temp = list(np.ravel(results))
    return jsonify(temp)


if __name__ == '__main__':
    app.run()
