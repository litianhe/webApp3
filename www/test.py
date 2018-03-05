def xf():
    yield 1,'a';
    yield 2,'b';
    yield 3,'c';
    yield 4,'d';

def fr():
    print('fr');
    yield from xf();

for x,y in fr():
    print(x,y);