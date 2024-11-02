class errors:
    class StatNonExistentError(Exception):
        def __init__(self):
            self.err_id = 1
        def __str__(self):
            return "Statistic does not exist!"