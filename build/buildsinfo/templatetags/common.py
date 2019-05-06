from django import template

register = template.Library()


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""


@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])


@register.tag(name='has')
def has_var(parser, token):
    """
    {% has some_var in ['123','456'] %}
    """
    print("token is ", token)
    parts = token.split_contents()
    print(parts)
    sublastbuild = str([lastbuild[0] for lastbuild in parts[3]])
    print(sublastbuild)
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'has' tag must be of the form: {% has <var_name> = <var_value_list> %}")

    return SetVarNode(parts[1], sublastbuild)
