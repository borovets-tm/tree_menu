from typing import Any, Optional
from django import template
from django.db.models import QuerySet

from app_menu.models import Category


register = template.Library()


def made_menu(total_list: Any, elements_list: list, ordering_list: list, elem_id: int, obj_id: int) -> None:
    """
    Функция рекурсивно создает меню, добавляя элементы в список на основе их категории и порядка.

    :param total_list: Это переменная, содержащая список объектов, представляющих все меню.
    :type total_list: Any
    :param elements_list: Параметр `elements_list` представляет собой список, который будет заполнен подсписками,
    содержащими информацию о каждом пункте меню. Каждый подсписок будет содержать идентификатор элемента и его
    форматированный заголовок, который включает соответствующее количество символов отступа в зависимости от положения
    элемента в иерархии меню.
    :type elements_list: list
    :param ordering_list: Это список, содержащий порядок, в котором категории должны отображаться в меню. Функция
    использует этот список для определения уровня отступа каждой категории в меню.
    :type ordering_list: list
    :param elem_id: Параметр elem_id представляет собой целое число, представляющее идентификатор обрабатываемого
    элемента меню.
    :type elem_id: int
    :param obj_id: obj_id — целочисленный параметр, представляющий идентификатор категории в меню. Он используется в
    функции для фильтрации total_list для получения всех объектов, принадлежащих к этой категории в указанном меню. Он
    также используется для определения уровня отступа для каждого элемента в elements_list
    :type obj_id: int
    """
    category_list = total_list.filter(menu_id=elem_id, category_id=obj_id)
    for i_obj in category_list:
        elements_list.append([
            i_obj.id, '    ' * (ordering_list.index(obj_id) + 1) + '|' + '____' + i_obj.title
        ])
        if i_obj.id in ordering_list:
            made_menu(total_list, elements_list, ordering_list, elem_id, i_obj.id)


@register.simple_tag(takes_context=True)
def draw_menu(context: dict, menu_name: str) -> str:
    """
    Функция рисует меню на основе заданного имени меню и контекста, используя данные из модели категорий.

    :param context: Параметр контекста — это словарь, содержащий информацию о текущем запросе и его контексте. Он
    используется для передачи данных между представлениями, шаблонами и промежуточным ПО в Django.
    :type context: dict
    :param menu_name: Название меню, которое нужно отрисовать.
    :type menu_name: str
    :return: Пустая строка.
    """
    total_list: QuerySet = Category.objects.select_related('menu').all()
    menu_list: list = list(set(map(lambda x: x.menu, total_list.filter(menu__title__exact=menu_name))))
    elements_list: list = []
    ordering_list: list = []
    pk: Optional[int] = context['request'].__dict__['resolver_match'][2].get('pk')
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
