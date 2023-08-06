from dataclasses import dataclass, field
from louvre_face.config import Config
from typing import Dict, List
import uuid

# Classes that represent prediction results:


@dataclass
class BoundingBoxParams:
    """
    :var str TOP:
    :var str LEFT:
    :var str WIDTH:
    :var str HEIGHT:
    """
    TOP = 'top'
    LEFT = 'left'
    WIDTH = 'width'
    HEIGHT = 'height'


@dataclass
class BoundingBox:
    """
    :var str top:
    :var str left:
    :var str width:
    :var str height:
    :var int decimal_places:
    """
    top: float
    left: float
    width: float
    height: float
    decimal_places: int = Config.predictions_rounding_decimal_places

    def to_dict(self) -> Dict[str, str]:
        """
        Return as a dict with serialised values, so that MetadataUpdater can accept it.

        :rtype: Dict[str, str]
        """
        return {
            BoundingBoxParams.TOP: str(round(self.top, self.decimal_places)),
            BoundingBoxParams.LEFT: str(round(self.left, self.decimal_places)),
            BoundingBoxParams.WIDTH: str(round(self.width,
                                               self.decimal_places)),
            BoundingBoxParams.HEIGHT:
            str(round(self.height, self.decimal_places))
        }


@dataclass
class PreditionResult:
    """
    Face detection prediction result.

    :param List[BoundingBox] bounding_boxes: Bounding boxes
    """
    bounding_boxes: List[BoundingBox] = field(default_factory=lambda: [])

    @property
    def faces(self) -> bool:
        """
        Whether faces were detected.
        
        :rtype: bool
        """
        return bool(len(self.bounding_boxes))


# Log-friendly classes that encapsulate the information of incoming HTTP requests


@dataclass
class Request:
    """
    Represent an incoming request.

    :param str endpoint: Endpoint name
    :param str image_identifier: Image identifier 
    """
    endpoint: str
    image_identifier: str

    def __post_init__(self):
        """Generate a unique request ID to make easier the tracking of a particular request."""
        self.request_id = str(uuid.uuid4())

    def __str__(self) -> str:
        raise NotImplementedError()


@dataclass
class EndpointRequest(Request):
    """
    Represent an incoming request.

    :param str endpoint: Endpoint name
    :param str image_identifier: Image identifier 
    :param bool using_production_images: Whether to use production images
    """
    using_production_images: bool

    def __str__(self) -> str:
        return \
f'''
{self.__class__.__name__}:
request_id= {str(self.request_id)};
endpoint= {str(self.endpoint)};
ImageId= {str(self.image_identifier)};
using_production_images= {str(self.using_production_images)};
'''


@dataclass
class PluginEndpointRequest(Request):
    """
    Represent an incoming request triggered by PluginTrigger.

    :param str endpoint: Endpoint name
    :param str image_identifier: Image identifier 
    :param str plugin_id: Plugin identifier
    """
    plugin_id: str

    def __str__(self) -> str:
        return \
f'''
{self.__class__.__name__}:
request_id= {str(self.request_id)};
endpoint= {str(self.endpoint)};
ImageId= {str(self.image_identifier)};
PluginId= {str(self.plugin_id)};
'''
