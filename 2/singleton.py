def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance

if __name__ == '__main__':
    from minitest import *

    @singleton
    class TestClass:
        x = 100

    with test(object.must_true):
        (TestClass() is TestClass() is TestClass).must_true()
        TestClass().x = 50
        (TestClass().x == 50 == TestClass.x).must_true()
