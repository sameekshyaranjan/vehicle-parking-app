from sqlalchemy.engine import make_url


def sqlalchemy_database_url(value):
    url = make_url(value)
    if url.drivername in {'postgres', 'postgresql'}:
        return url.set(drivername='postgresql+psycopg')
    return url
