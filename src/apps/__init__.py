# import models to generate migrations
from apps.user.models import TestModel, TestDocument

# add beanie models to document_models (if you are using mongodb)
document_models = [
    TestDocument,
]
