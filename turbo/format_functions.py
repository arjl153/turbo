import pprint

from prettytable import PrettyTable

import turbo.constants


def _get_lines(data, cols, max_field_size=turbo.constants.MAX_FIELD_SIZE):
    t = PrettyTable(cols)
    for i in data:
        r = []
        for c in cols:
            y = i.get(c, "")
            if isinstance(y, list):
                try:
                    y = ",".join(y)
                except TypeError:
                    y = len(y)

            # Handle potential Unicode issues
            try:
                y = str(y)  # Convert to string for consistent handling
            except (TypeError, ValueError):
                # Handle potential non-string conversion errors
                y = str(len(y))  # Fallback to string representation of length

            if y and (c in ["created_at", "updated_at"]):
                y = y.strptime(y, "YYYY-MM-DD HH:mm:ss")
                y = "{}Z".format(y)
            else:
                y = str(y)

            y = (y[:max_field_size] + "..") if len(y) > max_field_size else y
            r.append(y)
        t.add_row(r)

    yield str(t)


def raw_pprint(rv, cols=None):
    pprint(rv)


def ztable(rv, cols):
    for l in _get_lines(rv, cols):
        print(l)
