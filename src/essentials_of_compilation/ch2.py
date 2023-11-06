from ch1 import InterpLint
from dataclasses import dataclass
from typing import Any

@dataclass
class Assign:
    var : 'Any'
    value : 'Any'

class InterpLvar(InterpLint):
    def interp_exp(self, e, env):
        match e:
            case InterpLint.Name(id):
                return env[id]
            case _:
                return super().interp_exp(e, env)
    
    def interp_stmt(self, s, env, cont):
        match s:
            case Assign([InterpLint.Name(id)], value):
                env[id] = self.interp_exp(value, env)
                return self.interp_stmts(cont ,env)
            case _:
                return super().interp_stmt(s, env, cont)

def interp_Lvar(p):
    return InterpLvar().interp(p)
