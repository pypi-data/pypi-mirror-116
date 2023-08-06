from typing import Optional, Text

from convo.shared.exceptions import CoreException 


class UnsupportedCommunicationModelError(CoreException):
    """Raised when a model is too old to be loaded.

    Attributes:
        message -- explanation of why the model is invalid
    """

    def __init__(self, message: Text, model_version: Optional[Text] = None) -> None:
        self.message = message
        self.model_version = model_version
        super(UnsupportedCommunicationModelError, self).__init__()

    def __str__(self) -> Text:
        return self.message


class AgentNotPrepared(CoreException):
    """Raised if someone tries to use an agent that is not ready.

    An agent might be created, e.g. without an interpreter attached. But
    if someone tries to parse a message with that agent, this exception
    will be thrown."""

    def __init__(self, message: Text) -> None:
        self.message = message
        super(AgentNotPrepared, self).__init__()
