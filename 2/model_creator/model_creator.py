class FieldInfo:
    __field_type__ = object


class StringField(FieldInfo):
    __field_type__ = str


class IntField(FieldInfo):
    __field_type__ = int


class ListField(FieldInfo):
    __field_type__ = list


class StronglyTypedFieldInfo(FieldInfo):

    def __init__(self, _type):
        self.__field_type__ = _type


class StronglyTypedField:
    "Emulate Strong Typed Field, default value - None"

    def __init__(self, _type, _name):
        self._type = _type
        self._name = _name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if isinstance(value, self._type):
            setattr(instance, self._name, value)
        else:
            raise TypeError('Field must be ' + self._type.__name__)

    def __delete__(self, instance):
        delattr(instance, self._name)


class ModelCreator(type):

    def __new__(cls, name, bases, namespace):
        stf = []
        for item in list(namespace.items()):
            if isinstance(item[1], FieldInfo):
                stf.append(item)
                namespace[item[0]] = StronglyTypedField(item[1].__field_type__, '_' + item[0])

        result = super(ModelCreator, cls).__new__(cls, name, bases, namespace)
        setattr(result, '__init__', ModelCreator.get_init(result, stf))
        return result

    @staticmethod
    def get_init(result, stf):
        def __init__(self, *args, **kwargs):
            for field in stf:
                value = kwargs.pop(field[0], None)
                setattr(self, '_' + field[0], value)
            super(result, self).__init__(*args, **kwargs)
        return __init__


if __name__ == '__main__':
    class Person(metaclass=ModelCreator):
        age = IntField()
        name = StringField()


    class Student(Person):
        marks = ListField()

    s = Student()
    s.name = 'asdf'
    s.age = 10
    s.marks = list(range(10))
    print(s.name)
