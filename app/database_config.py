from urllib import parse
import boto3
from sqlalchemy import create_engine, event
from app.constants import AWS_REGION


CONNECTION_ARGS = {
    "prod": {
        "sslmode": "verify-full",
        "sslrootcert": "rds-ca-2019-root.pem"
    }
}


def get_db_url(app):
    db_auth_token = generate_db_user_password(app)
    db_url = f"postgresql+psycopg2://{app.config['DB_USER_NAME']}:{parse.quote(db_auth_token)}" \
             f"@{app.config['DB_HOST_NAME']}:{app.config['DB_PORT']}/{app.config['DB_NAME']}"
    print(app.config["ENVIRONMENT"])
    print(db_url)
    kw = {
        'user': app.config['DB_USER_NAME'],
        'password': parse.quote(db_auth_token)
    }
    return db_url, kw


def generate_db_user_password(app):
    if app.config["ENVIRONMENT"] in ["prod"]:
        rds_client = boto3.client(service_name="rds", region_name=AWS_REGION)
        db_auth_token = rds_client.generate_db_auth_token(
            DBHostname=app.config["DB_HOST_NAME"],
            Port=app.config['DB_PORT'],
            DBUsername=app.config['DB_USER_NAME']
        )
        return db_auth_token
    return app.config["DB_PASSWORD"]


def create_connector_engine(app):
    def create_db_engine(url, options):
        connection_retry = 0
        max_connection_retries = 5
        while connection_retry < max_connection_retries:
            db_url, kw = get_db_url(app)
            try:
                engine = create_engine(db_url,
                                       **options,
                                       echo=False,
                                       pool_size=50,
                                       max_overflow=1000,
                                       connect_args=CONNECTION_ARGS.get(
                                           app.config["ENVIRONMENT"],
                                           {}))

                @event.listens_for(engine, "do_connect")
                def on_connect(dialect, conn_rec, cargs, cparams):
                    cparams['password'] = generate_db_user_password(app)
                return engine

            except Exception as e:
                connection_retry += 1
                print("Connection error:", e)
    return create_db_engine