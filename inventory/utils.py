# utils.py

import locale


def format_mileage(mileage):
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        formatted_mileage = locale.format_string("%d", mileage, grouping=True)
        return formatted_mileage
    except (ValueError, locale.Error):
        return mileage  # Return the original mileage if formatting fails


def format_price(price):
    try:

        crores = price // 10000000
        lacs = (price % 10000000) // 100000

        if crores == 0:
            return f"{lacs} lacs"
        elif lacs == 0:
            return f"{crores} crore"
        else:
            return f"{crores} crore {lacs} lacs"
    except (ValueError, locale.Error):
        return price  # Return the original price if formatting fails
