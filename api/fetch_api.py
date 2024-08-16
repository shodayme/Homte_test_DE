from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from logger.loggerfactory import LoggerFactory
import json

class FastApp:
    def __init__(self, database_url, log_file):
        self.database_url = database_url
        self.log_file = log_file
        self.engine = create_engine(self.database_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = LoggerFactory(self.log_file).get_logger()
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
                res = db.execute(text("SELECT * from organizations order by id desc limit 10;")).fetchall()
                if res:
                    self.logger.info("Data fetched successfully.")
                else:
                    self.logger.warning("Table exists but has no data. Returning empty list")
                return [dict(_._mapping) for _ in res]
            except Exception as e:
                self.logger.error(f"failed to fetch data from db: {type(e).__name__} -- {str(e)}")
                return json.dumps("failed to fetch data from db. please check the api_logs for more details")

    def get_app(self):
        return self.app

if __name__ == "__main__":
# Initialize the app
    app = FastApp('postgresql://task_user:de_task_pwd@localhost:5432/task_db', './logs/api_logs.log')
    fast_app = app.get_app()
