from codetest.db.database import DB


class TestDatabase:

    def test_singleton_pattern(self):
        """Test to ensure singleton pattern of db class only allows for 
        one instance of a class -- despite  being called multiple times
        """
        db1 = DB()
        db2 = DB()
        db3 = DB()
        assert db1 == db2 == db3