"""Assign short typeable labels to targets (Vimium / Shortcat style)."""

CHARS = "asdfjklghweruio"


def make_labels(count: int) -> list[str]:
    if count <= 0:
        return []
    if count <= len(CHARS):
        return list(CHARS[:count])
    labels: list[str] = []
    for first in CHARS:
        for second in CHARS:
            labels.append(first + second)
            if len(labels) >= count:
                return labels
    return labels[:count]
