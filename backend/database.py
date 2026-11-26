from sqlalchemy.engine import make_url


def sqlalchemy_database_url(value):
    url = make_url(value)
    if url.drivername in {'postgres', 'postgresql'}:
        return url.set(drivername='postgresql+psycopg')
    if url.drivername == 'mysql':
        return url.set(drivername='mysql+pymysql')
    return url
