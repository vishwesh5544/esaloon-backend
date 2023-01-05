class TokenUtils:

    @staticmethod
    def get_token_from_header(self, auth_header: str) -> str:
        prefix = "Bearer"
        bearer, _, token = auth_header.partition(' ')
        if bearer != prefix:
            raise ValueError('Invalid Token')

        return token
