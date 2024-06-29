import asyncio
import re
import string
from typing import List, Optional, Set

from fastapi import UploadFile

import phonenumbers
from phonenumbers import NumberParseException

from src.accounts.models import User

from ..utils.constants import FILE_PARAMETERS
from ..utils.custom_error import ImageError

# from email_validator import validate_email, EmailNotValidError


def validate_emails(email: str) -> bool:
    """
    Validate the format of an email address using a regular expression pattern.
    Args:
        email (str): The email address to be validated.
    Returns:
        bool: True if the email address matches the expected format, otherwise raises an exception.
    Raises:
        Exception: If the email address does not match the expected format.
    Email Format:
    - The email address should contain one or more groups of alphanumeric characters, optionally followed
      by a period (.), hyphen (-), or underscore (_), and then followed by an at symbol (@).
    - After the at symbol, there should be one or more alphanumeric characters, hyphens, or digits,
      followed by a period (.) and a top-level domain (TLD) with at least two characters.
    Example:
    >>> validate_email("john.doe@example.com")
    True
    >>> validate_email("invalid-email")
    Exception: email is not correct
    """
    pattern = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )

    if not re.fullmatch(pattern, email):
        raise ValueError(
            "email is not in the correct format eg --- john.doe@example.com"
        )
    return email
    # try:
    #     valid = validate_email(email)
    #     if valid:
    #         return True
    # except EmailNotValidError as e:
    #     return e


# class Pas
def validate_password(passwords: str) -> bool:
    """
    Validates a password based on specified criteria.
    Args:
        passwords (str): The password to be validated.
    Returns:
        bool: True if the password meets all criteria, otherwise raises a ValueError.
    Raises:
        ValueError: If the password does not meet the specified criteria.
    Password Criteria:
    - The password length must be greater than 8 characters.
    - The password must contain at least one lowercase letter.
    - The password must contain at least one uppercase letter.
    - The password must contain at least one digit.
    - The password must contain at least one special character (e.g., @, #, $, %, &).
    Example:
    >>> validate_password("Passw0rd@")
    True
    """
    if len(passwords) <= 8:
        raise ValueError("password should be more than than 8 characters")
        # detail="password should be more than than 8 characters"
        # return detail

    is_uppercase: bool = False
    is_lowercase: bool = False
    is_digit: bool = False
    is_special_char: bool = False

    special_char = set(string.punctuation)
    for password in passwords:
        is_uppercase |= any(char.isupper() for char in password)
        # logger.info(is_uppercase)

        is_lowercase |= any(char.islower() for char in password)
        # logger.debug(is_lowercase)

        is_digit |= any(char.isdigit() for char in password)
        # logger.debug(is_digit)

        is_special_char |= any(char in special_char for char in password)
        # logger.debug(is_special_char)

    if not is_lowercase:
        detail = "password must contain a lowercase letter (eg a,b,c etc)"
        raise ValueError(detail)

    if not is_uppercase:
        detail = "password must contain an uppercase letter (eg A,B,C etc)"
        raise ValueError(detail)

    if not is_digit:
        detail = "password must contain a digit (eg 1,2,4 etc)"
        raise ValueError(detail)

    if not is_special_char:
        detail = "password must contain a special character (eg @, #, $, %, & etc)"
        raise ValueError(detail)

    return True


def image_validator(file: UploadFile) -> bool:
    file.file.seek(0, 2)
    file_size = file.file.tell()

    asyncio.run(file.seek(0))
    max_size = FILE_PARAMETERS.MAX_FILE_SIZE
    if file_size > FILE_PARAMETERS.MAX_FILE_SIZE:
        f"File size exceeds the maximum allowed size ({max_size/(1024*1024)} MB)."

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise ImageError("Invalid file type")

    return True


def validate_phone_number(value):
    if value is not None:
        try:
            parsed_number = phonenumbers.parse(value, None)
            formatted_number = phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.E164
            )
            return formatted_number
        except (NumberParseException, Exception) as e:
            raise ValueError("Invalid phone number format", str(e))


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in FILE_PARAMETERS.ALLOWED_EXTENSIONS
    )


def file_validator(file: UploadFile):
    """
    Validate the uploaded file.

    Parameters:
    - file: An instance of the uploaded file (e.g., Flask's FileStorage).

    Raises:
    - ValueError: If the file is not valid.
    """
    if file is None:
        raise ValueError("No file provided.")

    if not allowed_file(file.filename):
        raise ValueError(
            "Invalid file format. Allowed formats: {}".format(
                ", ".join(FILE_PARAMETERS.ALLOWED_EXTENSIONS)
            )
        )

    max_size = FILE_PARAMETERS.MAX_FILE_SIZE  # 5 MB
    file.file.seek(0, 2)
    file_size = file.file.tell()

    asyncio.run(file.seek(0))
    if file_size > max_size:
        raise ValueError(
            "File size exceeds the maximum allowed size ({} MB).".format(
                max_size / (1024 * 1024)
            )
        )

    return True


def user_validator(values: Optional[Set[int]]) -> List[int]:
    # a util function to validate if user is not a super-admin
    if len(values) == 1:
        try:
            user: User = User.valid_objects.get(id=list(values)[0])
            if user.is_superadmin:
                raise ValueError("Permission Denied: You cannot perform this operation")
        except User.DoesNotExist:
            raise ValueError("The user was not found")

        return values

    validated_users = []
    for value in values:
        try:
            user: User = User.valid_objects.get(id=value)
            if not user.is_superadmin:
                validated_users.append(value)
        except User.DoesNotExist:
            pass
    return validated_users
