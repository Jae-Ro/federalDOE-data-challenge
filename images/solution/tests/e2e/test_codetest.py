from codetest.main import run as codetest_run
from codetest.db.database import DB
import codetest.utils.log_utils as log_utils
import codetest.utils.io_utils as io_utils
import os

class TestEnd2End:
    db = DB()
    db.create_engine('codetest')
    logger = log_utils.get_custom_logger('TestEnd2End')
    data_dir = "/data"
    if not os.path.exists(os.path.join(data_dir, 'people.csv')):
        data_dir = '../../data'
    
    # expected results
    actual_a = io_utils.read_json(os.path.join(data_dir, 'summary_output.json'))
    actual_b = io_utils.read_json(os.path.join(data_dir, 'summary_output_extra.json'))
    
    def test_run_end2end(self):
        """Function to run codetest solution end-to-end and cleanup before and after
        """
        args = {"data_dir": self.data_dir}
        self.logger.debug('Truncating Tables to Run End2End Test')
        self.db.truncate_table('people')
        self.db.truncate_table('places')

        self.logger.debug('Running End2End Function')
        report_a, report_b = codetest_run(args)
        self.logger.debug(f"End-to-End Results:\n\t{report_a}\n\t{report_b}")

        # assertions
        assert report_a == self.actual_a
        assert report_b == self.actual_b

        self.logger.debug('Truncating Tables to Cleanup End2End Test')
        self.db.truncate_table('people')
        self.db.truncate_table('places')
