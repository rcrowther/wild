#!/usr/bin/python3


def tmpl_print(data):
    return "\nprint{0}".format(data[0])

def tmpl_println(data):
    return "\nprintln{0}".format(data[0])


def tmpl_add(data):
    if (len(data) > 1):
        return "\nadd {0},{1}".format(data[0], data[1])
    else:
        return "+{0}".format(data[0])

def tmpl_sub(data):
    if (len(data) > 1):
        return "\nsub {0},{1}".format(data[0], data[1])
    else:
        return "-{0}".format(data[0])

def tmpl_mul(data):
    return "\nmul {0},{1}".format(data[0], data[1])

def tmpl_div(data):
    return "\ndiv {0},{1}".format(data[0], data[1])

def tmpl_if(data, mark):
    return "\ncmp{0} {1}".format(data[0], mark)

def tmpl_call(data):
    return "\mov AX, {0}".format(data[0])

def writeNothing(params, body):
    return ''

# will need to be more here, scaled register protection,
# paremeter retieval etc.
def tmpl_call_function(mark):
    return "\ncall {0}".format(mark)

# may need to be more here, scaled register protection,
# paremeter retieval etc.
def tmpl_define_function_head(mark):
    return "\n {0}".format(mark)

def tmpl_define_function_tail():
    return "\nret\n"

def tmpl_define_data_move(fromRegister, toRegister):
    return "\nmov {0},{1}".format(fromRegister, toRegister)

def tmpl_push(data):
    return "\npush {0}".format(data[0])

def tmpl_pop(data):
    return "\npop {0}".format(data[0])

stock_tmpl = {
'stack_push': tmpl_push,
'stack_pop': tmpl_pop,
'function_call': tmpl_call_function,
'function_head': tmpl_define_function_head,
'function_tail': tmpl_define_function_tail,
'data_move': tmpl_define_data_move
}

tmpl = {
'TREE_ROOT' : writeNothing,
'block' : writeNothing,
'$$plus$' : tmpl_add,
'$$minus$' : tmpl_sub,
'$$mult$' : tmpl_mul,
'$$divide$' : tmpl_div, 
'print' : tmpl_print,
'println' : tmpl_println

}

word_tmpl = {
'TREE_ROOT' : '',
'block' : '',
'$$plus$' : 'add',
'$$minus$' : 'sub',
'$$mult$' : 'mul',
'$$divide$' : 'div',
'stack_pop' : 'pop',
'stack_push' : 'push',
'data_move' : 'mov'
}
