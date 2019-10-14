class new_draw:
    def __enter__(self):
        pushStyle()

    def __exit__(self, *args, **kw):
        popStyle()


w, h = 700, 700
