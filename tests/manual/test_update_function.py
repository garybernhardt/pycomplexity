def foo():
    x if x else x if x else x if x else x if x else x if x else x if x else x
    # Delete this line, then save. The function should go from yellow to
    # green. Then undo and save. The *whole thing* should go back to yellow.
    x if x else x
    pass
    pass
    pass

