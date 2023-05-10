from django import template

from app_menu.models import Category


register = template.Library()


def made_menu(total_list, elements_list, ordering_list, elem_id, obj_id):
    category_list = total_list.filter(menu_id=elem_id, category_id=obj_id)
    for i_obj in category_list:
        elements_list.append([
            i_obj.id, '    ' * (ordering_list.index(obj_id) + 1) + '|' + '____' + i_obj.title
        ])
        if i_obj.id in ordering_list:
            made_menu(total_list, elements_list, ordering_list, elem_id, i_obj.id)


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    total_list = Category.objects.select_related('menu').all()
    menu_list = list(set(map(lambda x: x.menu, total_list.filter(menu__title__exact=menu_name))))
    elements_list = []
    ordering_list = []
    pk = context['request'].__dict__['resolver_match'][2].get('pk')
    if pk:
        first_element = total_list.get(id=pk)
        while first_element.category:
            ordering_list.append(first_element.id)
            first_element = total_list.get(id=first_element.category.id)
        ordering_list.append(first_element.id)
        ordering_list.reverse()
    for elem in menu_list:
        elements_list.append([0, elem.title])
        category_list = total_list.filter(menu_id=elem.id)
        for obj in category_list.filter(category_id=None):
            elements_list.append([obj.id, '|____' + obj.title])
            if obj.id in ordering_list:
                made_menu(total_list, elements_list, ordering_list, elem.id, obj.id)
    context['elements_list'] = elements_list
    return ''
