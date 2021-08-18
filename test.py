a = []

def test(a):
  for _ in a:
    yield _

print(list(test(a)))