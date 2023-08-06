import unittest
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from covid_data.db.queries import (
    create_case,
    create_country,
    create_county,
    create_province,
    place_exists,
)
from covid_data.test_utils import MockDB


class TestPlaceExists(TestCase):
    mock_id = "TestID"

    def test_connect_called(self):
        """Place exists should call connect once"""
        mockDb = MockDB()

        mockDb.execute_return = [{"id": 0}]

        mockDb.cursor = MagicMock(return_value=mockDb)

        place_exists("Test", mockDb)  # type: ignore

        mockDb.cursor.assert_called_once()

    def test_execute_called(self):
        """Place exists should call execute once"""
        mockDb = MockDB()

        mockDb.execute = MagicMock(return_value=[{"id": 0}])

        place_exists("Test", mockDb)  # type: ignore

        mockDb.execute.assert_called_once()

    def test_should_return_id(self):
        """Place exists should return id if exists"""
        mockDb = MockDB()

        mockDb.execute_return = [{"id": self.mock_id}]

        res = place_exists("Test", mockDb)  # type: ignore

        self.assertEqual(self.mock_id, res)

    def test_should_return_none(self):
        """Place exists should return none if empty result"""
        mockDb = MockDB()

        mockDb.execute_return = []

        res = place_exists("Test", mockDb)  # type: ignore

        self.assertIsNone(res)


class TestCreateCountry(TestCase):
    mock_id = "TestID"

    execute_return = [{"id": mock_id}]

    mock_country = {
        "name": "Test Country",
        "lat": 20.1234,
        "lng": 120.1234,
    }

    def test_connect_called(self):
        """Create country should call connect once"""
        mockDb = MockDB()

        mockDb.execute_return = self.execute_return

        mockDb.cursor = MagicMock(return_value=mockDb)

        create_country(self.mock_country, mockDb)  # type: ignore

        mockDb.cursor.assert_called_once()

    def test_execute_called(self):
        """Create country should call execute once"""
        mockDb = MockDB()
        mockDb.execute_return = self.execute_return

        mockDb.execute = MagicMock(return_value=mockDb)

        create_country(self.mock_country, mockDb)  # type: ignore

        mockDb.execute.assert_called_once()

    def test_should_return_inserted_id(self):
        """Create country should return inserted id"""
        mockDb = MockDB()

        mockDb.execute_return = self.execute_return

        res = create_country(self.mock_country, mockDb)  # type: ignore

        self.assertEqual(res, self.mock_id)


class TestCreateProvince(TestCase):
    mock_id = "TestID"

    execute_return = [{"id": mock_id}]

    mock_province = {
        "name": "Test Province",
        "lat": 20.1234,
        "lng": 120.1234,
    }

    def test_connect_called(self):
        """Create province should call connect once"""
        mockDb = MockDB()

        mockDb.execute_return = self.execute_return

        mockDb.cursor = MagicMock(return_value=mockDb)

        create_province(self.mock_province, mockDb)  # type: ignore

        mockDb.cursor.assert_called_once()

    def test_execute_called(self):
        """Create province should call execute once"""
        mockDb = MockDB()
        mockDb.execute_return = self.execute_return

        mockDb.execute = MagicMock(return_value=mockDb)

        create_province(self.mock_province, mockDb)  # type: ignore

        mockDb.execute.assert_called_once()

    def test_should_return_inserted_id(self):
        """Create province should return inserted id"""
        mockDb = MockDB()

        mockDb.execute_return = self.execute_return

        res = create_province(self.mock_province, mockDb)  # type: ignore

        self.assertEqual(res, self.mock_id)


class TestCreateCounty(TestCase):
    mock_id = "TestID"

    execute_return = [{"id": mock_id}]

    mock_county = {
        "name": "Test County",
        "lat": 20.1234,
        "lng": 120.1234,
    }

    def test_connect_called(self):
        """Create county should call connect once"""
        mockDb = MockDB()

        mockDb.execute_return = self.execute_return

        mockDb.cursor = MagicMock(return_value=mockDb)

        create_county(self.mock_county, mockDb)  # type: ignore

        mockDb.cursor.assert_called_once()

    def test_execute_called(self):
        """Create county should call execute once"""
        mockDb = MockDB()
        mockDb.execute_return = self.execute_return

        mockDb.execute = MagicMock(return_value=mockDb)

        create_county(self.mock_county, mockDb)  # type: ignore

        mockDb.execute.assert_called_once()

    def test_should_return_inserted_id(self):
        """Create county should return inserted id"""
        mockDb = MockDB()

        mockDb.execute_return = self.execute_return

        res = create_county(self.mock_county, mockDb)  # type: ignore

        self.assertEqual(res, self.mock_id)


class TestCreateCase(TestCase):
    mock_case = {"type": "death", "amount": 10, "date": datetime.now(), "country_id": 1}

    def test_connect_called(self):
        """Create case should call connect once"""
        mockDb = MockDB()

        mockDb.cursor = MagicMock(return_value=mockDb)

        create_case(self.mock_case, mockDb)  # type: ignore

        mockDb.cursor.assert_called_once()

    def test_execute_called(self):
        """Create case should call execute once"""
        mockDb = MockDB()

        mockDb.execute = MagicMock(return_value=mockDb)

        create_case(self.mock_case, mockDb)  # type: ignore

        mockDb.execute.assert_called_once()

    def test_should_return_true(self):
        """Create case should return True"""
        mockDb = MockDB()

        res = create_case(self.mock_case, mockDb)  # type: ignore

        self.assertTrue(res)


if __name__ == "__main__":
    unittest.main()
