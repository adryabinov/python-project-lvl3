def read(path, mode="r"):
    with open(path, mode) as f:
        result = f.read()
    return result
