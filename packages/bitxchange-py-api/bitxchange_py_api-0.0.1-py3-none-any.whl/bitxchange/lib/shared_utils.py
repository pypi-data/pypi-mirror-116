from bitxchange.errors import ParameterRequiredError
from bitxchange.errors import TargetPairError

from typing import Optional, Dict, Any


def remove_none_values(input) -> dict:
    # Removes any empty values from input dict and returns a clean dict
    resp = {}
    for kw in input.keys():
        if input[kw] is not None:
            resp[kw] = input[kw]
    return resp


def check_required_parameter(mandatory_params=None, **kwargs):
    """
    Take injected kwargs and validate that there are no empty values.

    If mandatory params are also injected then params will be checked to have
    all mandatory params present before checking for none values.
    """

    # If mandatory params have been passed check mand_params are in params
    if mandatory_params:
        missing_params = []
        for param in mandatory_params:

            if param not in kwargs:
                missing_params.append(param)

        if missing_params:
            raise ValueError(f"Following fields are missing as attributes: {','.join(missing_params)}")

    # validate all params have no None values
    for key, value in kwargs.items():
        if not value:
            raise ParameterRequiredError([key])


# Takes target_pair and validates they are active pair on the exchange
def validate_target_pair(
    target_pair: str,
    available_pairs: Optional[Dict[str, Any]] = None
):

    if not available_pairs:
        from bitxchange.spot import Spot

        spot = Spot()
        available_pairs = spot.available_trading_pairs()

    if target_pair not in available_pairs['combinations']:
        raise TargetPairError(target_pair) from None
    else:
        return str(target_pair)
