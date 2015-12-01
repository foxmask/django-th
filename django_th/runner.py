from django.conf import settings
from django.test.runner import DiscoverRunner


class DiscoverRunnerTriggerHappy(DiscoverRunner):
    """
    A Django test runner that uses unittest2 test discovery.
    """
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.

        Test labels should be dotted Python paths to test modules, test
        classes, or test methods.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        """
        self.setup_test_environment()
        for installed_app in settings.INSTALLED_APPS:
            test_labels = test_labels + (installed_app,)
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases()
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)
