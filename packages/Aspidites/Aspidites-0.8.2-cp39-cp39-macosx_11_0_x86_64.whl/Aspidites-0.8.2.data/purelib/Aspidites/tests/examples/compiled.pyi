from Aspidites.woma import *
from Aspidites._vendor import F as F
from Aspidites._vendor.RestrictedPython import safe_builtins as safe_builtins
from Aspidites._vendor.contracts import contract as contract, new_contract as new_contract
from Aspidites.monads import Maybe as Maybe, SafeDiv as SafeDiv, SafeExp as SafeExp, SafeMod as SafeMod, Surely as Surely, Undefined as Undefined
from collections.abc import Generator
from pyrsistent import PClass as PClass, PRecord as PRecord, m as m, s as s, v as v
from typing import Any

procedure: None
coroutine: Generator
number: Any

def Add(x: int = ..., y: int = ...) -> int: ...
def Yield123() -> coroutine: ...
def Hello() -> procedure: ...
def Hello2() -> coroutine: ...

D: Any
G: Any
C: Any
x: Any
y: Any
z: Any
scala: Any
val: Any
denom: int
div_by_zero: Any
mod_zero: Any
div_by_zero2: Any
mod_zero2: Any
