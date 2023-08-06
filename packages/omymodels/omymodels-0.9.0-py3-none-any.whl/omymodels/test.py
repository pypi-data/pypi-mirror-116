from omymodels import convert_models


models_from = """

class MaterialType(str, Enum):

    article = "article"
    video = "video"


@dataclass
class Material:

    id: int
    title: str
    description: str
    link: str
    type: MaterialType
    additional_properties: Union[dict, list]
    created_at: datetime.datetime
    updated_at: datetime.datetime


"""

result = convert_models(models_from)
print(result)
