from disposable_email_domains import blocklist
from emailrep import EmailRep

from pyoti.classes import EmailAddress


class DisposableEmails(EmailAddress):
    """DisposableEmails Email Address Reputation

    This class checks if an email address is contained within a set of known disposable email domains.
    """

    def check_email(self):
        """Checks if email domain is a known disposable email service.

        :return: dict
        """
        domain = self.email.split("@")[1]
        info = {"email": self.email}
        if domain in blocklist:
            info["disposable"] = True
        else:
            info["disposable"] = False

        return info


class EmailRepIO(EmailAddress):
    """EmailRepIO Email Address Reputation

    EmailRep is a system of crawlers, scanners, and enrichment services that
    collects data on email addresses, domains, and internet personas. EmailRep uses
    hundreds of data points from social media profiles, professional networking
    sites, dark web credential leaks, data breaches, phishing kits, phishing emails,
    spam lists, open mail relays, domain age and reputation, deliverability, and
    more to predict the risk of an email address.
    """

    def __init__(self, api_key):
        EmailAddress.__init__(self, api_key=api_key)

    def _api(self):
        """Instantiates EmailRep API"""

        emlrep = EmailRep(self.api_key)

        return emlrep

    def check_email(self):
        """Checks Email Address reputation"""

        emlrep = self._api()
        response = emlrep.query(self.email)

        return response
