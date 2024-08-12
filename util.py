def validate_alc_content(alc_content):
    if alc_content < 8:
        return True
    else:
        return False


def validate_beer_brand(brand):
    return brand.isalnum()
