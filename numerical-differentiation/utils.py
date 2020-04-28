import parser


def wrap_code(code, modules):
    """
    Compiles given line to Python bytecode and returns function which evaluates given bytecode with given modules in
    environment.
    """
    func_bytecode = parser.expr(code).compile()

    env = globals().copy()

    for m in modules:
        exec('import {}'.format(m), env)

    def func(x):
        return eval(func_bytecode, env, {'x': x})

    return func
