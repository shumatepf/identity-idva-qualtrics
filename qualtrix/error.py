"""
Custom Qualtrics Error. For specific raise/catch use.
"""
class QualtricsError(Exception):
    def __init__(self, message):
        super().__init__(message)
