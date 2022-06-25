from __future__ import annotations
from typing import Type

class Symbol():
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    dictionary = {}

    def to_string(self) -> str:
        return self.name

    
    def symbol(name: str) -> Symbol:
        symbol: Symbol = Symbol.dictionary.get(name)
        
        if symbol is None:
            symbol = Symbol(name)
            Symbol.dictionary[name] = symbol

        return symbol

class MethodEntry():

    def __init__(self, type: Type) -> None:
        self.return_type = type
        self.locals = {}
        self.param = {}
        self.param_list = []

    def get_params(self):
        return self.param

    def get_param_by_name(self, id: str) -> Type:
        return self.param.get(Symbol.symbol(id).to_string())

    def get_locals(self):
        return self.locals

    def get_local_by_name(self, id: str) -> Type:
        return self.locals.get(Symbol.symbol(id).to_string())        

    def get_num_params(self) -> int:
        return len(self.param_list)

    def get_param_by_position(self, pos: int) -> Type:
        return self.param_list[pos]

    def get_return_type(self) -> Type:
        return self.return_type

    def add_local(self, id: str, type: Type) -> bool:
        if(self.contains_local(Symbol.symbol(id).to_string()) or self.contains_param(Symbol.symbol(id).to_string())):
            return False
        else:
            self.locals[Symbol.symbol(id).to_string()] = type

        return True


    def add_param(self, id: str, type: Type) -> bool:
        if(self.contains_param(Symbol.symbol(id).to_string())):
            return False
        else:
            self.param[Symbol.symbol(id).to_string()] = type
            self.param_list.append(type)
        
        return True

    def contains_local(self, key: str) -> bool:
        return key in self.locals.keys()

    def contains_param(self, key: str) -> bool:
        return key in self.param.keys()




class ClassEntry():

    def __init__(self, supper_class_id: str = None):
        self.fields = {}
        self.methods = {}
        self.supper_class_id = supper_class_id


    def get_supper_class_id(self):
        return self.supper_class_id

    def get_fields(self):
        return self.fields

    def get_field(self, id: str) -> Type:
        return self.fields.get(Symbol.symbol(id).to_string())
    
    def get_methods(self):
        return self.methods

    def get_method(self, id: str) -> MethodEntry:
        return self.methods.get(Symbol.symbol(id).to_string())    
    
    def add_var(self, id : str, type: Type) -> bool:
        if(self.contains_field(Symbol.symbol(id).to_string())):
            return False
        else:
            self.fields[Symbol.symbol(id).to_string()] = type
        
        return True

    def add_method(self, id: str, entry: MethodEntry) -> bool:
        if(self.contains_method(Symbol.symbol(id).to_string())):
            return False
        else:
            self.methods[Symbol.symbol(id).to_string()] = entry
    
        return True

    def contains_field(self, key: str) -> bool:
        return key in self.fields.keys()
    

    def contains_method(self, key: str) -> bool:
        return key in self.methods.keys()



class SymbolTable():
    
    def __init__(self) -> None:
        self.class_scopes = {}
        self.curr_class = None
        self.curr_method = None
        self.curr_class_name = None
        self.curr_method_name = None

    def contains_class(self, key: str) -> bool:
        return key in self.class_scopes.keys()

    def get_class_entry(self, id: str) -> ClassEntry:
        return self.class_scopes.get(Symbol.symbol(id).to_string())

    def set_curr_class(self, id: str) -> None:
        self.curr_class = self.class_scopes.get(Symbol.symbol(id).to_string());      
        self.curr_class_name = id
        self.curr_method = None
        self.curr_method_name = None

    def set_curr_method(self, id: str):
        self.curr_method = self.curr_class.get_method(id)
        self.curr_method_name = id

    def add_scope(self, id: str, entry: ClassEntry) -> bool:
        self.curr_class = entry
        self.curr_class_name = id
        self.curr_method = None
        self.curr_method_name = None
        
        if(self.contains_class(Symbol.symbol(id).to_string())):
            return False
        else:
            self.class_scopes[Symbol.symbol(id).to_string()] = entry

        return True

    def add_extends_entry(self, id: str, supper_class_id: str) -> None:

        base: ClassEntry = self.get_class_entry(Symbol.symbol(id).to_string())
        supper_class: ClassEntry = self.get_class_entry(Symbol.symbol(supper_class_id).to_string())

        if supper_class is not None:
            for supper_field_id in supper_class.get_fields().keys():
                base.add_var(supper_field_id, supper_class.get_field(supper_field_id))
            
            for supper_method_id in supper_class.get_methods().keys():
                base.add_method(supper_method_id, supper_class.get_method(supper_method_id))


    def add_method(self, id: str, entry: MethodEntry) -> bool:
        self.curr_method = entry
        self.curr_method_name = id
        
        if(self.curr_class.add_method(id, entry)):
            return True
        else:
            return False
        

    def add_field(self, id: str, type: Type) -> bool:
        return self.curr_class.add_var(id, type)

    def add_param(self, id: str, type: Type) -> bool:
        return self.curr_method.add_param(id, type)

    def add_local(self, id: str, type: Type) -> bool:
        return self.curr_method.add_local(id, type)
