def save(content, path: str, mode="w+"):
    with open(path, mode) as f:
        return f.write(content)
