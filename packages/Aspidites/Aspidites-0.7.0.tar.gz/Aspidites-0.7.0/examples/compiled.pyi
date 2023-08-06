from Aspidites.woma import *
from Aspidites._vendor import F as F
from Aspidites.monads import Surely as Surely, Undefined as Undefined
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
