extra = {'city': 'Beijing', 'job': 'Engineer'}


def person(kw):
    kw['city'] = 'qingdao'


person(extra)
print(extra)


def test(a, b):
    print(a + b)


a = 100
b = 200
test(88, b)
