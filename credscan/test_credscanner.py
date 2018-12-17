"""
A test class to verify the credential checker
"""

import tokenize

import pylint.testutils
from pylint.interfaces import HIGH

import credscan

class TestCredScannerChecker(pylint.testutils.CheckerTestCase):
    """
    Contains test cases for the CredentialChecker
    """

    CHECKER_CLASS = credscan.CredentialChecker

    def test_simple_strings_not_credentials(self):
        """
        Checks that the checker doesn't raise a message for regular strings
        """

        tokens = [
            tokenize.TokenInfo(
                tokenize.STRING, "This is my string!", (0, 0), (0, 0), ""
            )]

        with self.assertNoMessages():
            self.checker.process_tokens(tokens)

    def test_identifies_credential(self):
        """
        Tests whether the checker correctly raises a message for a credential
        """

        tokens = [
            tokenize.TokenInfo(
                tokenize.STRING, "p@ssw0rd!", (0, 0), (0, 0), ""
            )]

        with self.assertAddsMessages(
                pylint.testutils.Message(
                    msg_id='E9001',
                    line=0,
                    node=None,
                    args='p@ssw0rd!',
                    confidence=HIGH
                ),
        ):
            self.checker.process_tokens(tokens)

    def test_simple_strings_are_not_passwords(self):
        """
        Tests whether simple strings with 2 character classes are passwords
        """

        tokens = [
            tokenize.TokenInfo(
                tokenize.STRING, "this-is-not-my-password", (0, 0), (0, 0), ""
            ),
            tokenize.TokenInfo(
                tokenize.STRING, "123456789", (0, 0), (0, 0), ""
            ),
            tokenize.TokenInfo(
                tokenize.STRING, "!@#$%^&**", (0, 0), (0, 0), ""
            )]

        with self.assertNoMessages():
            self.checker.process_tokens(tokens)
