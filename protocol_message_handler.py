import enum


X = 0
Y = 1
KEY_VALUE_SEPARATOR = ": "
FIELD_SEPARATOR = "\n"
X_COORDINATE = "X-COOR"
Y_COORDINATE = "Y-COOR"
STATUS_SEPARATOR = ", "


class ProtocolException(Exception):
    pass


class Status(enum.Enum):
    CORRECT = 0
    INCORRECT = 1
    FULL_SUB = 2
    VICTORY = 3


class ProtocolMessagesHandler:
    def __init__(self, version):
        self.version = version

    def _get_message_header(self, message_type):
        return f"VERSION: {self.version}\nTYPE: {message_type}\n"

    def get_ready_message(self):
        return self._get_message_header("READY")

    def get_attempt_message(self, location):
        return self._get_message_header("ATTEMPT") + \
        f"{X_COORDINATE}: {location[X]}\n{Y_COORDINATE}: {location[Y]}\n"

    def get_answer_message(self, status, location):
        return self._get_message_header("ANSWER") + \
        f"STATUS: {self._status_to_text(status)}\n{X_COORDINATE}: {location[X]}\n{Y_COORDINATE}: {location[Y]}\n"

    def _status_to_text(self, status):
        if status == Status.CORRECT or status == Status.INCORRECT:
            return status.name
        if status == Status.FULL_SUB or status == Status.VICTORY:
            return f"{Status.CORRECT.name}, {status.name}"

    def _parse_message_to_dict(self, message: str):
        try:
            fields = message.split(FIELD_SEPARATOR)
            parsed_fields = {}
            for field in fields[:-1]:
                key, value = field.split(KEY_VALUE_SEPARATOR)
                parsed_fields[key] = value
        except ValueError as error:
            raise ProtocolException() from error
        return parsed_fields

    def parse_message_type(self):
        pass

    def parse_attempt_message(self, message):
        fields = self._parse_message_to_dict(message)
        try:
            return int(fields[X_COORDINATE]), int(fields[Y_COORDINATE])
        except KeyError as error:
            raise ProtocolException() from error

    def parse_answer_message(self, message):
        fields = self._parse_message_to_dict(message)
        try:
            status = fields["STATUS"].split(STATUS_SEPARATOR)
            if "CORRECT" in status:
                if "FULL-SUB" in status:
                    return Status.FULL_SUB
                elif "VICTORY" in status:
                    return Status.VICTORY
                return Status.CORRECT
            return Status.INCORRECT
        except KeyError as error:
            raise ProtocolException() from error
