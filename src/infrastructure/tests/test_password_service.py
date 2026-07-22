from src.containers import Container


class TestPasswordService:
    def test_hash_password_returns_non_empty_string_different_from_plain(
        self, container: Container
    ):
        # given
        service = container.password_service()
        plain_password = "SecurePassword123!"

        # when
        hashed_password = service.hash(plain_password)

        # then
        assert isinstance(hashed_password, str)
        assert hashed_password != plain_password
        assert len(hashed_password) > 0

    def test_hash_password_generates_unique_hashes_for_same_password(
        self, container: Container
    ):
        # given
        service = container.password_service()
        plain_password = "SecurePassword123!"

        # when
        hash_one = service.hash(plain_password)
        hash_two = service.hash(plain_password)

        # then
        assert hash_one != hash_two

    def test_verify_password_returns_true_for_matching_password(
        self, container: Container
    ):
        # given
        service = container.password_service()
        plain_password = "SecurePassword123!"

        # when
        hashed_password = service.hash(plain_password)
        is_valid = service.verify(plain_password, hashed_password)

        # then
        assert is_valid is True

    def test_verify_password_returns_false_for_incorrect_password(
        self, container: Container
    ):
        # given
        service = container.password_service()
        plain_password = "CorrectPassword123!"
        wrong_password = "WrongPassword456!"

        # when
        hashed_password = service.hash(plain_password)
        is_valid = service.verify(wrong_password, hashed_password)

        # then
        assert is_valid is False
