from typing import Iterator


class MissingFieldError(Exception):
    pass


def get_field_values(line: str, field_names: list[str]) -> list[str | None]:
    res: list[str | None] = []
    for name in field_names:
        prefix = "\x09" + name + "="
        i1 = line.find(prefix)
        if i1 == -1:
            res.append(None)
            continue
        i1 += len(prefix)
        i2 = line.find("\x09", i1 + 1)
        if i2 == -1:
            res.append(line[i1:])
        else:
            res.append(line[i1:i2])
    return res


def read_lines_from_end(filename: str, buffer_size: int = 8192) -> Iterator[str]:
    """Yield lines from a binary file in reverse order."""
    with open(filename, "rb") as f:
        f.seek(0, 2)  # Move to the end of the file
        position = f.tell()
        buffer = b""

        while position > 0:
            # Determine read size and adjust position
            read_size = min(buffer_size, position)
            position -= read_size
            f.seek(position)
            chunk = f.read(read_size) + buffer

            # Split lines
            lines = chunk.split(b"\n")
            buffer = lines.pop(0)  # First element might be incomplete

            for line in reversed(lines):
                if line:
                    yield line.decode()
        if buffer:  # Yield remaining content
            yield buffer.decode()


def iterate_tskv_lines_within_time_range(
    filename: str, time_field_name: str, since: float | None, until: float | None
) -> Iterator[str]:
    for line in read_lines_from_end(filename):
        ts_str = get_field_values(line, [time_field_name])[0]
        if ts_str is None:
            raise MissingFieldError(f'Field "{time_field_name}" not found')
        ts = float(ts_str)
        if until is not None and ts > until:
            continue
        if since is not None and ts < since:
            break
        yield line
