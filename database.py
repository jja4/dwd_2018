import pony.orm as porm
import database
from datetime import date
import station_names

conn_url = 'postgresql://@localhost:5432/weather2'
db = porm.Database()

class Station(db.Entity):
    stations_id   = porm.PrimaryKey(int, auto=False)
    von_datum     = porm.Optional(date)
    bis_datum     = porm.Optional(date)
    stationshoehe = porm.Optional(int)
    geobreite     = porm.Optional(float)
    geolaenge     = porm.Optional(float)
    stationsname  = porm.Required(str)
    bundesland    = porm.Optional(str)
    measurements  = porm.Set('DailyMeasurement')
    
    @classmethod
    def in_Berlin(cls):
        return cls.select(lambda s: 'Berlin' in s.stationsname)

    
class DailyMeasurement(db.Entity):
    mess_datum  = porm.Required(date)
    stations_id = porm.Required(Station)
    qn_3        = porm.Optional(int)  # quality level of next columns
    fx          = porm.Optional(float)
    fm          = porm.Optional(float)
    qn_4        = porm.Optional(int)
    rsk         = porm.Optional(float)
    rskf        = porm.Optional(float)
    sdk         = porm.Optional(float)
    shk_tag     = porm.Optional(float)
    nm          = porm.Optional(float)
    vpm         = porm.Optional(float)
    pm          = porm.Optional(float)
    tmk         = porm.Optional(float)
    upm         = porm.Optional(float)
    txk         = porm.Optional(float)
    tnk         = porm.Optional(float)
    tgk         = porm.Optional(float)
    
    porm.PrimaryKey(mess_datum, stations_id)
    
    
class DailyPrediction(db.Entity):
    id                 = porm.PrimaryKey(int, auto=True)
    website            = porm.Required(str)
    city               = porm.Required(str)
    date_of_aquisition = porm.Required(str)
    date_for_which_weather_is_predicted = porm.Required(str)
    temperature_max    = porm.Required(float)
    temperature_min    = porm.Required(float)
    wind_speed         = porm.Optional(float, nullable=True)
    humidity           = porm.Optional(float, nullable=True)
    precipation_per    = porm.Optional(float, nullable=True)
    precipation_l      = porm.Optional(float, nullable=True)
    wind_direction     = porm.Optional(str, 3, nullable=True)
    condition          = porm.Optional(str, nullable=True)
    snow               = porm.Optional(float, nullable=True)
    UVI                = porm.Optional(int, unsigned=True)
    
    
class HourlyPrediction(db.Entity):
    id                  = porm.PrimaryKey(int, auto=True)
    website             = porm.Required(str)
    city                = porm.Required(str)
    date_of_acquisition = porm.Required(str)
    date_for_which_weather_is_predicted = porm.Required(str)
    temperature         = porm.Required(float)
    wind_speed          = porm.Optional(float)
    humidity            = porm.Optional(float)
    precipitation_per   = porm.Optional(float)
    precipitation_l     = porm.Optional(float)
    wind_direction      = porm.Optional(str, 3)
    condition           = porm.Optional(str)
    snow                = porm.Optional(float)
    UVI                 = porm.Optional(int, unsigned=True)
    
    
class DailyPeriodPrediction(db.Entity):
    id                  = porm.PrimaryKey(int, auto=True)
    website             = porm.Required(str)
    city                = porm.Required(str)
    date_of_acquisition = porm.Required(str)
    date_for_which_weather_is_predicted = porm.Required(str)
    temperature         = porm.Required(float)
    wind_speed          = porm.Optional(float)
    precipitation_per   = porm.Optional(float)
    precipitation_l     = porm.Optional(float)
    wind_direction      = porm.Optional(str, 3)
    condition           = porm.Optional(str)
    
    
def set_up_connection(db, db_name, user='', host=''):
    '''
    Sets up a connection with the database server.
    '''
    db.bind(provider='postgres', user='', password='', host='', database=db_name)
    db.generate_mapping(create_tables = True)