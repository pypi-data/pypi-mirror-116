from hestia_earth.schema import InputStatsDefinition
from hestia_earth.utils.lookup import get_table_value, download_lookup
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.input import _new_input
from hestia_earth.models.utils.dataCompleteness import _is_term_type_incomplete
from hestia_earth.models.utils.term import get_liquid_fuel_terms
from hestia_earth.models.utils.site import valid_site_type
from . import MODEL

TERM_ID = 'machineryInfrastructureDepreciatedAmountPerCycle'


def _get_input_value_from_term(inputs: list, term_id: str):
    val = find_term_match(inputs, term_id, None)
    return val.get('value', [0])[0] if val is not None else 0


def get_value(country_id: dict, cycle: dict):
    lookup = download_lookup('region.csv', True)
    liquid_fuels = get_liquid_fuel_terms()

    in_lookup = country_id in list(lookup.termid)
    logger.debug('Found lookup data for Term: %s? %s', country_id, in_lookup)

    if in_lookup:
        hdi = safe_parse_float(get_table_value(lookup, 'termid', country_id, 'hdi'), None)
        if hdi is not None:
            # if hdi >= 0.8 take use Diesel KG from row 1, if <0.8 use row 2
            machinery_usage = 11.5 if float(hdi) >= 0.8 else 23
            fuel_use = sum([_get_input_value_from_term(cycle.get('inputs', []), term_id) for term_id in liquid_fuels])
            return fuel_use/machinery_usage if fuel_use > 0 else None
    return None


def _input(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    input = _new_input(TERM_ID, MODEL)
    input['value'] = [value]
    input['statsDefinition'] = InputStatsDefinition.MODELLED.value
    return input


def _run(cycle: dict):
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    value = get_value(country_id, cycle)
    return [_input(value)] if value is not None else []


def _should_run(cycle: dict):
    should_run = valid_site_type(cycle.get('site', {})) and _is_term_type_incomplete(cycle, TERM_ID)
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else []
