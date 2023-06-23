from django import template

register = template.Library()


@register.filter
def teacher_gender_to_string(value):
    if value == 1:
        return '男'
    elif value == 2:
        return '女'
    else:
        return ''


@register.filter
def teacher_title_to_string(value):
    title_dict = {
        0: '',
        1: '博士后',
        2: '助教',
        3: '讲师',
        4: '副教授',
        5: '特任教授',
        6: '教授',
        7: '助理研究员',
        8: '特任副研究员',
        9: '副研究员',
        10: '特任研究员',
        11: '研究员',
    }
    return title_dict.get(value, '')


@register.filter
def paper_type_to_string(value):
    if value == 1:
        return 'Full paper'
    elif value == 2:
        return 'Short paper'
    elif value == 3:
        return 'Poster paper'
    elif value == 4:
        return 'Demo paper'
    else:
        return ''


@register.filter
def paper_level_to_string(value):
    if value == 1:
        return 'CCF-A'
    elif value == 2:
        return 'CCF-B'
    elif value == 3:
        return 'CCF-C'
    elif value == 4:
        return '中文 CCF-A'
    elif value == 5:
        return '中文 CCF-B'
    elif value == 6:
        return '无级别'
    else:
        return '无级别'


@register.filter
def project_type_to_string(value):
    if value == 0:
        return ''
    elif value == 1:
        return '国家级项目'
    elif value == 2:
        return '省部级项目'
    elif value == 3:
        return '市厅级项目'
    elif value == 4:
        return '企业合作项目'
    elif value == 5:
        return '其他类型项目'
    else:
        return '无类型'


@register.filter
def class_type_to_string(value):
    if value == 0:
        return ''
    elif value == 1:
        return '本科生课程'
    elif value == 2:
        return '研究生课程'
    else:
        return '无类型'


@register.filter
def class_semester_to_string(value):
    if value == 0:
        return ''
    elif value == 1:
        return '春季学期'
    elif value == 2:
        return '夏季学期'
    elif value == 3:
        return '秋季学期'
    else:
        return '无类型'
