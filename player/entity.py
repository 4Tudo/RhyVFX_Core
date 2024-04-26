from ursina import *

chartEntity = []


from ursina import *


def find_nearest_specific_entity(arrow):
    try:
        desired_entities = [entity for entity in chartEntity if entity.trackId == arrow.arrowId]
        distances = [(entity, distance(arrow, entity)) for entity in desired_entities]
        closest_entity, closest_distance = min(distances, key=lambda x: x[1])
        return closest_entity
    except Exception:
        return None


# find_nearest_specific_entity()