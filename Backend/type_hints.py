### Type hints ###

my_string_variable = "My String Variable"
print(my_string_variable)
print(type(my_string_variable))

### ahora es del tipo int, esto pasa porque es de tipado dinamico ###
my_string_variable = 5
print(my_string_variable)
print(type(my_string_variable))

### especificando el tipo de dato a la variable le estamos diciendo al editor que va a llevar nuestra variable###
my_typed_variable: int = "My  typed String varible" 
### es mas si colocamos my_typed_variable. el editor nos ayuda mostrandonos metodos del tipo de dato que definimos antes###
print(my_typed_variable)
print(type(my_typed_variable))

### es buena practica para fastApi ayuda para backend 
my_typed_variable: str = 5
print(my_typed_variable)
print(type(my_typed_variable))