
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COMA DESPEDIDA PALABRA PUNTO SALUDO SUJETOoracion : SALUDO COMA SUJETO PALABRA complemento PUNTO DESPEDIDAcomplemento : PALABRA complementocomplemento : PALABRA'
    
_lr_action_items = {'SALUDO':([0,],[2,]),'$end':([1,10,],[0,-1,]),'COMA':([2,],[3,]),'SUJETO':([3,],[4,]),'PALABRA':([4,5,6,],[5,6,6,]),'PUNTO':([6,7,8,],[-3,9,-2,]),'DESPEDIDA':([9,],[10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'oracion':([0,],[1,]),'complemento':([5,6,],[7,8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> oracion","S'",1,None,None,None),
  ('oracion -> SALUDO COMA SUJETO PALABRA complemento PUNTO DESPEDIDA','oracion',7,'p_oracion','tbl-sint.py',84),
  ('complemento -> PALABRA complemento','complemento',2,'p_complemento_recursivo','tbl-sint.py',102),
  ('complemento -> PALABRA','complemento',1,'p_complemento_base','tbl-sint.py',108),
]
