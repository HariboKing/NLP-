from nlp_trainer_support.runtime_setup import initialize_runtime_database
from nlp_trainer_support.web import create_app


initialize_runtime_database()
application = create_app()
app = application
