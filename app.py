import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
from sqlalchemy import create_engine, func
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

# 2. Create an app
app = Flask(__name__)


# 3. List the routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# 3. Define static routes
@app.route("/api/v1.0/precipitation")
def precip_records():
    """Return the precipitation count by Station"""
    session = Session(engine)
    date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date).all()
    session.close()
    year_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        year_precip.append(precip_dict)

    return jsonify(year_precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return the Stations"""
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    all_names = list(np.ravel(results))
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > date).filter(Measurement.station == 'USC00519281').all()
    session.close()
    tobs= list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def summary(start):
    session = Session(engine)
    startdate = start
    sel = [func.avg(Measurement.tobs), 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).all()
    session.close()
    summary= list(np.ravel(results))
    return jsonify(summary)


@app.route("/api/v1.0/<start>/<end>")
def summarywithend(start, end):
    session = Session(engine)
    startdate = start
    enddate = end
    sel = [func.avg(Measurement.tobs), 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= startdate, Measurement.date <= enddate).all()
    session.close()
    summarywithend= list(np.ravel(results))
    return jsonify(summarywithend)

if __name__ == '__main__':
    app.run(debug=True)

