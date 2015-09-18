from django.shortcuts import render


def montaMensagemErro(form):
    errors = form.errors
    msg = '<ul>'
    for fe in errors:
        msg += '<li>'
        msg += form.fields[fe].label
        msg += '<ul><li>' + \
               ''.join(errors[fe]) + \
               '</li></ul>'
        msg += '</li>'
    msg += '<ul>'
    return msg
