from src.containers import Container


class TestPasswordService:
    def test_hash_password(self, container: Container):
        # given
        service = container.password_service()
        plain_password = "SecurePassword123!"

        # when
        hash_one = service.hash(plain_password)
        hash_two = service.hash(plain_password)

        # then
        assert hash_one != plain_password
        assert hash_two != plain_password
        assert hash_one != hash_two

    def test_verify_password(self, container: Container):
        # given
        service = container.password_service()
        plain_password = "SecurePassword123!"
        wrong_password = "WrongPassword456!"

        # when
        hashed_password = service.hash(plain_password)

        # then
        assert service.verify(plain_password, hashed_password) is True
        assert service.verify(wrong_password, hashed_password) is False
