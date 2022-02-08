import facebook

class Facebook:
    """This handles auth token validation with facebook
    """

    @staticmethod
    def validate(auth_token):
        """Query the graph api to get user information

        Args:
            auth_token ([type]): [description]
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request("/me?fields=email,first_name,last_name")
            return profile
        except Exception as e:
            print(e)
            return "The token is invalid or expired"