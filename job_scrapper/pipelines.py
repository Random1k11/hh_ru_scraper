from sqlalchemy.orm import sessionmaker

from job_scrapper.models import db_connect, create_table, Vacancy


class JobScrapperPipeline:

    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        vacancy = Vacancy()

        vacancy.title = item["title"]
        vacancy.salary = item["salary"]
        vacancy.company = item["company"]
        vacancy.company_link = item["company_link"]
        vacancy.employment_mode = item["employment_mode"]
        vacancy.description = item["description"]
        vacancy.tags = item["tags"]
        vacancy.creation_time = item["creation_time"]
        vacancy.link = item["link"]
        vacancy.platform = item["platform"]

        exist_vacancy = session.query(Vacancy).filter_by(link=vacancy.link).first()
        if not exist_vacancy:
            try:
                session.add(vacancy)
                session.commit()

            except Exception:
                session.rollback()
                raise

            finally:
                session.close()
        return item
