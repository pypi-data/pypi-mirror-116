import operator
from functools import reduce

from django.db.models import Q

from huscy.attributes.models import AttributeSet
from huscy.attributes.services import get_attribute_schema
from huscy.pseudonyms.services import get_subjects
from huscy.recruitment.models import AttributeFilterSet, ParticipationRequest


def create_attribute_filterset(subject_group):
    return AttributeFilterSet.objects.create(subject_group=subject_group)


def update_attribute_filterset(attribute_filterset, filters):
    if attribute_filterset.participation_requests.exists():
        return AttributeFilterSet.objects.create(subject_group=attribute_filterset.subject_group,
                                                 filters=filters)
    attribute_filterset.filters = filters
    attribute_filterset.save()

    return attribute_filterset


def apply_attribute_filterset(attribute_filterset):
    attribute_sets = _filter_attributesets_by_filterset(attribute_filterset)
    subjects = get_subjects([attribute_set.pseudonym for attribute_set in attribute_sets])
    subjects = _exclude_invited_subjects(subjects, attribute_filterset)
    return subjects


def _filter_attributesets_by_filterset(attribute_filterset):
    filters = _get_filters(attribute_filterset)
    return AttributeSet.objects.filter(*filters)


def _get_filters(attribute_filterset):
    attribute_schema = get_attribute_schema()

    for attribute_name, filter_values in attribute_filterset.filters.items():
        exclude = False

        if attribute_name.startswith('-'):
            attribute_name = attribute_name[1:]
            exclude = True

        attribute_type = _get_attribute_type(attribute_schema.schema, attribute_name)

        if attribute_type in ['integer', 'number']:
            lookup = f'attributes__{attribute_name}__range'
        elif attribute_type == 'array':
            lookup = f'attributes__{attribute_name}__contains'
        else:
            lookup = f'attributes__{attribute_name}'

        q = reduce(operator.or_, (Q(**{lookup: filter_value}) for filter_value in filter_values))

        if exclude:
            q = ~Q(q)

        yield q


def _get_attribute_type(schema, attribute_name):
    path = ['properties'] + attribute_name.replace('__', '__properties__').split('__')
    attribute = reduce(operator.getitem, path, schema)
    return attribute['type']


def _exclude_invited_subjects(subjects, attribute_filterset):
    participation_request_pseudonyms = ParticipationRequest.objects.filter(
        attribute_filterset__subject_group__experiment=attribute_filterset.subject_group.experiment,
        status=ParticipationRequest.STATUS.get_value('invited')
    ).values_list('pseudonym', flat=True)
    invited_subjects = get_subjects(participation_request_pseudonyms)
    return subjects.difference(invited_subjects)
