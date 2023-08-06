def class_to_flux(c: str) -> float:
    """
    Maps a flare class (e.g. B6, M, X9) to a GOES flux value.
    Source: i4Ds/SDOBenchmark

    :param c: class as string
    :return: flux value as float
    """

    goes_classes = ['quiet', 'A', 'B', 'C', 'M', 'X']

    if c == 'quiet':
        return 1e-9

    decade = goes_classes.index(c[0]) - 9
    sub = float(c[1:]) if len(c) > 1 else 1

    return round(10 ** decade * sub, 10)
