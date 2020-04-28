import parser


def wrap_code(code, modules):
    func_bytecode = parser.expr(code).compile()

    env = globals().copy()

    for m in modules:
        exec('import {}'.format(m), env)

    def func(x):
        return eval(func_bytecode, env, {'x': x})

    return func
