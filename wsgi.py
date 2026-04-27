import nlp_trainer_support.branding_extension  # noqa: F401
import nlp_trainer_support.deletion_extension  # noqa: F401
import nlp_trainer_support.game_extension  # noqa: F401
import nlp_trainer_support.game_map_extension  # noqa: F401
import nlp_trainer_support.reviews_extension  # noqa: F401
import nlp_trainer_support.world_models_extension  # noqa: F401
import nlp_trainer_support.content_admin_extension  # noqa: F401
import nlp_trainer_support.content_editor_access_extension  # noqa: F401
import nlp_trainer_support.content_question_management_extension  # noqa: F401
from nlp_trainer_support.runtime_setup import initialize_runtime_database
from nlp_trainer_support.web import create_app


initialize_runtime_database()
application = create_app()
app = application
