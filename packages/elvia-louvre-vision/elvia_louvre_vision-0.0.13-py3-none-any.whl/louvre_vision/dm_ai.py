"""Module with classes that represent data structures."""

from azure.cognitiveservices.vision.customvision.training.models import Iteration
from dataclasses import dataclass
from louvre_vision.data_models import ImageRegion
from typing import Dict
import uuid

from .config import Config

# Classes that represent prediction results:


@dataclass
class PredictionResult:
    probability: float

    def to_dict(self) -> Dict[str, str]:
        raise NotImplementedError()


@dataclass
class ClassificationPredictionResult(PredictionResult):
    tag_name: str

    def to_dict(self) -> Dict[str, str]:
        return {
            'probability':
            str(
                round(self.probability,
                      Config.predictions_rounding_decimal_places)),
            'tag_name':
            self.tag_name
        }


@dataclass
class ObjectDetectionPredictionResult(PredictionResult):
    region: ImageRegion

    def to_dict(self) -> Dict[str, str]:
        return {
            'probability':
            str(
                round(self.probability,
                      Config.predictions_rounding_decimal_places)),
            'tag_name':
            self.region.tag_name,
            'bounding box':
            str(self.region.bounding_box)
        }


# Log-friendly classes that encapsulate the information of incoming HTTP requests


@dataclass
class Request:

    endpoint: str
    model_name: str
    image_identifier: str

    def __post_init__(self):
        """Generate a unique request ID to make easier the tracking of a particular request."""
        self.request_id = str(uuid.uuid4())

    def __str__(self) -> str:
        raise NotImplementedError()


@dataclass
class EndpointRequest(Request):

    using_production_images: bool
    probability_threshold: float

    def __str__(self) -> str:
        return \
f'''
{self.__class__.__name__}:
request_id= {str(self.request_id)};
endpoint= {str(self.endpoint)};
model_name= {str(self.model_name)};
ImageId= {str(self.image_identifier)};
using_production_images= {str(self.using_production_images)};
probability_threshold= {str(self.probability_threshold)};
'''


@dataclass
class PluginEndpointRequest(Request):

    plugin_id: str

    def __str__(self) -> str:
        return \
f'''
{self.__class__.__name__}:
request_id= {str(self.request_id)};
endpoint= {str(self.endpoint)};
model_name= {str(self.model_name)};
ImageId= {str(self.image_identifier)};
PluginId= {str(self.plugin_id)};
'''


# Classes that have all that is needed to run predictions with either ClassificationPrediction
# or ObjectDetectionPrediction


@dataclass
class PredictionRequest:

    endpoint_request: EndpointRequest
    model: Iteration


@dataclass
class PluginPredictionRequest:

    endpoint_request: PluginEndpointRequest
    model: Iteration
