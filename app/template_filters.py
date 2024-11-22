from django.template.defaulttags import register

@register.filter(name='get_sum_dict_values')
def get_sum_dict_values(dict, key):
    return sum(dict[key].values())