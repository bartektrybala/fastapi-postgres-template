import pytest

from src.domain.exceptions import map_specific_exception_regex


class MyError(Exception):
    pass


class TestMapSpecificExceptionRegex:
    def test_matching_error_message_regex(self) -> None:
        # given
        @map_specific_exception_regex(
            from_=ValueError,
            to=MyError,
            from_message=r"Key \(email\)=\((.*?)\)\s+already exists\.",
            to_message="Duplicate email detected",
        )
        def raise_duplicate_email_error() -> None:
            raise ValueError(
                '(psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "ix_user_email"\nDETAIL:  Key (email)=(new@email.com) already exists.\n\n'  # noqa: E501
            )

        # when & then
        with pytest.raises(MyError, match="Duplicate email detected"):
            raise_duplicate_email_error()

    def test_message_doesnt_match_regex(self) -> None:
        # given
        @map_specific_exception_regex(
            from_=ValueError,
            to=MyError,
            from_message=r"Key \(username\)=\((.*?)\)\s+already exists\.",
            to_message="Duplicate username detected",
        )
        def raise_non_matching_error() -> None:
            raise ValueError("DETAIL:  Key (email)=(test@example.com) already exists.")

        # when & then
        with pytest.raises(ValueError, match="test@example.com"):
            raise_non_matching_error()

    def test_no_exception_regex(self) -> None:
        # given
        @map_specific_exception_regex(
            from_=ValueError,
            to=MyError,
            from_message=r"Specific value error",
            to_message="My specific error",
        )
        def foo_no_error() -> None:
            pass

        # when & then
        foo_no_error()

    def test_no_message_error_regex(self) -> None:
        # given
        @map_specific_exception_regex(
            from_=ValueError,
            to=MyError,
            from_message=r"dummy",
            to_message="My specific error",
        )
        def raise_no_message_error() -> None:
            raise ValueError

        # when & then
        with pytest.raises(ValueError):
            raise_no_message_error()

    def test_different_exception_type_regex(self) -> None:
        # given
        @map_specific_exception_regex(
            from_=ValueError,
            to=MyError,
            from_message=r"some regex",
            to_message="mapped message",
        )
        def raise_type_error() -> None:
            raise TypeError("This is a type error")

        # when & then
        with pytest.raises(TypeError, match="This is a type error"):
            raise_type_error()
