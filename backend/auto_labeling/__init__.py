# Patch the CustomRESTRequestModel in the pipeline to provide defaults
from typing import Optional
import auto_labeling_pipeline.models as alp_models

# Get the original model
OriginalCustomRESTRequestModel = alp_models.CustomRESTRequestModel

# Create a wrapper that provides defaults
class CustomRESTRequestModelWithDefaults(OriginalCustomRESTRequestModel):
    """
    Override with default values for optional fields.
    This makes params, headers, and body truly optional (not required) in the schema.
    """
    params: Optional[dict] = {}
    headers: Optional[dict] = {}
    body: Optional[dict] = {}

# Replace in the factory's search path by monkey-patching the find method
from auto_labeling_pipeline.models import RequestModelFactory, RequestModel

# Store original find method
_original_find = RequestModelFactory.find

# Create new find method that returns CustomRESTRequestModelWithDefaults for "Custom REST Request"
@classmethod
def _patched_find(cls, model_name: str):
    if model_name == "Custom REST Request":
        return CustomRESTRequestModelWithDefaults
    return _original_find(model_name)

# Replace the find method
RequestModelFactory.find = _patched_find
