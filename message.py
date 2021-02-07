class Message:
    """
    holds message's sender id, receiver id and data
    """

    def __init__(self, data, sender_id, receiver_id):
        """
        :param data: object
        :param sender_id: str
        :param receiver_id: str
        """
        self.data = data
        self.sender_id = sender_id
        self.receiver_id = receiver_id
