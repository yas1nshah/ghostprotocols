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
        if price < 10000000:
            return "30 lacs"

        crores = price // 10000000
        lacs = (price % 10000000) // 100000
        formatted_price = crores + lacs / 10.0
        return f"{formatted_price:.1f} crores"
    except (ValueError, locale.Error):
        return price  # Return the original price if formatting fails
