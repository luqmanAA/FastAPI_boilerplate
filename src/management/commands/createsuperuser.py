from getpass import getpass

from termcolor import colored

from src.accounts.models import User
from src.utils.validators import validate_emails
from src.config import SessionLocal


def colored_input(prompt, color="white"):
    return input(colored(prompt, color))


def createsuperuser() -> User:
    exit_message = colored("Exiting the superuser creation process.", "red")
    """Create a superuser."""
    with SessionLocal() as db:
        # while True:
        try:
            while True:
                try:
                    email = colored_input("Enter your email: ", "cyan")
                    validate_emails(email)

                    existing_email = db.query(User).filter(User.email == email).first()
                    if existing_email is None:
                        break
                    else:
                        print(colored(f"Error: User '{email}' already exists.", "red"))
                        user_choice = input(
                            "Do you want to re-enter your email (yes/no): "
                        ).lower()
                        if user_choice != "yes":
                            print(exit_message)
                            return

                except ValueError as e:
                    print(colored(f"Error: {str(e)}", "red"))
                    user_choice = colored_input(
                        "Do you want to re-enter your email (yes/no): ", "yellow"
                    ).lower()
                    if user_choice != "yes":
                        print(exit_message)
                        return

            while True:
                try:
                    password_1 = getpass("Enter your password: ")
                    password_2 = getpass("Enter your password again: ")

                    if password_1 != password_2:
                        print(colored(f"password do not match", "red"))
                    else:
                        validate_password(password_2)
                        hashed_password = hash_password(password_2)
                        break
                except ValueError as e:
                    print(colored(f"Error: {str(e)}", "red"))
                    user_choice = colored_input(
                        "Do you want to re-enter your password (yes/no): ", "yellow"
                    ).lower()
                    if user_choice != "yes":
                        print(exit_message)
                        return

            while True:
                username = colored_input("Enter your username: ", "cyan")
                existing_username = (
                    db.query(User).filter(User.username == username).first()
                )
                if existing_username is None:
                    break
                else:
                    print(
                        colored(f"Error: Username '{username}' already exists.", "red")
                    )
                    user_choice = colored_input(
                        "Do you want to re-enter your username (yes/no): ", "yellow"
                    ).lower()
                    if user_choice != "yes":
                        print(exit_message)
                        return

            while True:
                first_name = colored_input("Enter your first name: ", "cyan")
                existing_first_name = (
                    db.query(User).filter(User.first_name == first_name).first()
                )
                if existing_first_name is None:
                    break
                else:
                    print(
                        colored(
                            f"Error: First name '{username}' already exists.", "red"
                        )
                    )
                    user_choice = input(
                        "Do you want to re-enter your first name (yes/no): "
                    )
                    if user_choice != "yes":
                        print(exit_message)
                        return

            while True:
                last_name = colored_input("Enter your last name: ", "cyan")
                existing_last_name = (
                    db.query(User).filter(User.last_name == last_name).first()
                )
                if existing_last_name is None:
                    break
                else:
                    print(
                        colored(
                            f"Error: Last Name '{last_name}' already exists.", "red"
                        )
                    )
                    user_choice = input(
                        "Do you want to re-enter your last name (yes/no): "
                    )
                    if user_choice != "yes":
                        print(exit_message)
                        return

            # Create the superuser
            user = User.objects.create(
                username=username,
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                is_verified=True,
            )
            # db.add(superuser)
            # db.commit()

            print(colored(f"User '{username}' created successfully.", "green"))

        except Exception as e:
            db.rollback()
            print(colored(f"Error: {str(e)}", "red"))


if __name__ == "__main__":
    # createsuperuser()
    pass
