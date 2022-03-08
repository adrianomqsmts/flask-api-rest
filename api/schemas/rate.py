"""Schema do Modelo de Avaliação."""
from marshmallow_enum import EnumField

from api.instances.ma import ma
from api.models.rate import RateModel, TypeRate


# Responsável por serealizar os dados do banco de dados no envio e na recepção destes dados
# https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
class RateSchema(ma.SQLAlchemyAutoSchema):
    """Schema de Serialização do modelo de Avaliação."""

    # https://stackoverflow.com/questions/44717768/how-to-serialise-a-enum-property-in-sqlalchemy-using-marshmallow
    rate_type = EnumField(TypeRate, by_value=True)

    class Meta:
        """Meta Class."""

        model = RateModel
        load_instance = True
