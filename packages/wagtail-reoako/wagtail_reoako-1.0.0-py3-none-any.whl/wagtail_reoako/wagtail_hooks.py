from draftjs_exporter.dom import DOM

import wagtail.admin.rich_text.editors.draftail.features as draftail_features

from wagtail.core import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler

from .urls import urlpatterns


@hooks.register('register_admin_urls')
def wagtail_reoako_urls():
    return urlpatterns


def reoako_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the reoako entities into a span tag.

    TODO:
        this is a bit ugly storing and display all this info since the headword & translation
        are only used by content editor in the cms. future state could just store id and fetch it
        from api when page is loaded.
    """
    return DOM.create_element('span', {
        'data-reoako-id': props.get('reoakoId'),
        'data-reoako-headword': props.get('reoakoHeadword'),
        'data-reoako-translation': props.get('reoakoTranslation'),
    }, props['children'])


class ReoakoEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the span tag into a Reoako entity, with the right data.
    """
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        """
        Take the ``stock`` value from the ``data-stock`` HTML attribute.
        """
        return {
            'reoakoTranslation': attrs.get('data-reoako-translation'),
            'reoakoHeadword': attrs.get('data-reoako-headword'),
            'reoakoId': attrs.get('data-reoako-id'),
        }


@hooks.register('register_rich_text_features')
def register_reoako_feature(features):
    features.default_features.append('reoako')
    feature_name = 'reoako'
    type_ = 'REOAKO'

    control = {
        'type': type_,
        'label': '',
        'description': 'Reoako',
        'icon': [
            '''
            M18.2822 114.286C18.2822 68.8406 55.1228 32 100.568 32H923.425C968.87 32 1005.71 
            68.8406 1005.71 114.286V813.714C1005.71 859.159 968.87 896 923.425 896H622.845L536.183 
            996.068C523.422 1010.8 500.564 1010.8 487.804 996.068L401.142 896H100.568C55.1228 896 18.2822 
            859.159 18.2822 813.714V672H443.593V524H443.59V430H443.593V301.438H509.406C565.752 301.438 
            593.024 325.719 593.024 370.344C593.024 414.75 565.752 437.062 509.856 
            437.062H444.59V513.188H514.815L602.265 672H710L611.957 497.875C664.472 476 693.547 431.594 
            693.547 370.344C693.547 281.312 632.918 224 528.113 224H346V671H18.2822V114.286Z
            '''
        ],
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['wagtail_reoako/js/reoako.js'],
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'span[data-reoako-id]': ReoakoEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: reoako_entity_decorator}},
    })
