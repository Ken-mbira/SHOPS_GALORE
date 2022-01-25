from google.auth.transport import requests
from google.oauth2 import id_token

class Google:
    """Google function to return user information
    """

    @staticmethod
    def validate(auth_token):
        """This queries the google oauth2 api to fetch the user information

        Args:
            auth_token ([type]): [description]
        """
        try:
            user_information = id_token.verify_oauth2_token(auth_token,requests.Request())

            if 'accounts.google.com' in user_information['iss']:
                return user_information

        except:
            return "The token is either invalid or expired"