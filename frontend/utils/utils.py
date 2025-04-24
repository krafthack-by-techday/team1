def get_price_area(metering_point_id: str) -> str | None:
    if metering_point_id != "":  # The default return value of the text widget -
        # until the user has entered their ID, we do not know the price area
        return "NO42"
    return None
