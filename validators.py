def validate_age(age):
    try:
        age = int(age)
        if age <= 18:
            return False, "Age must be greater than 18"
        return True, age
    except (ValueError, TypeError):
        return False, "Age must be a number"
