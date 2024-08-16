from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from logger.loggerfactory import LoggerFactory


class FastApp:
    def __init__(self, database_url, log_file):
        self.database_url = database_url
        self.log_file = log_file
        self.engine = create_engine(self.database_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = LoggerFactory().get_logger('api_logger', self.log_file)
        self.app = FastAPI()

        # Register routes
        self.register_routes()

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()

    def register_routes(self):
        @self.app.get("/read/first-chunk")
        def read_data(db: Session = Depends(self.get_db), limit: int = 100):
            try:
                self.logger.info("fetching 10 rows from organizations table ...")
                res = db.execute(text("SELECT * from organizations limit 10;")).fetchall()
                if res:
                    self.logger.info("Data fetched successfully.")
                else:
                    self.logger.warning("Table exists but has no data. Returning empty list")
                return [dict(r._mapping) for r in res]
            except Exception as e:
                self.logger.error(f"failed to fetch data from db: {type(e).__name__} -- {str(e)}")
                raise HTTPException(status_code=500,
                                    detail="Failed to fetch data from the database. Please check the api logs for more details.")

    def get_app(self):
        return self.app


def create_app():
    app_instance = FastApp('postgresql://task_user:de_task_pwd@localhost:5432/task_db', './logs/api_logs.log')
    return app_instance.get_app()


if __name__ == "__main__":
    # Initialize the app
    # app = FastApp('postgresql://task_user:de_task_pwd@localhost:5432/task_db', './logs/api_logs.log')
    fast_app = create_app()
