from django.conf import settings
from django.test.runner import DiscoverRunner


class DiscoverRunnerTriggerHappy(DiscoverRunner):
    """
    A Django test runner that uses unittest2 test discovery.
    """

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.
        Except those in TEST_RUNNER_WHITELIST tuple

        Test labels should be dotted Python paths to test modules, test
        classes, or test methods.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        """
        self.setup_test_environment()
        app_to_test = self.unwanted_apps()
        for installed_app in app_to_test:
            test_labels = test_labels + (installed_app,)
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases()
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)

    @staticmethod
    def unwanted_apps():
        installed_apps = frozenset(settings.INSTALLED_APPS)

        try:
            do_not_test = frozenset(settings.TEST_RUNNER_WHITELIST)
        except AttributeError:
            do_not_test = set()

        return installed_apps - do_not_test
