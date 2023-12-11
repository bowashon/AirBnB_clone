#!/usr/bin/python3
"""unittest for the basemodel"""
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def test_init(self):
        my_model = BaseModel()
        self.assertIsNotNone(my_model.created_at)
        self.assertIsNotNone(my_model.updated_at)
        self.assertIsNotNone(my_model.id)

    def testSave(self):
        my_model = BaseModel()

        created_update = my_model.updated_at
        current_update = my_model.save()
        self.assertNotEqual(created_update, current_update)

    def testTo_dict(self):
        my_model = BaseModel()
        obj_dict = my_model.to_dict()

        self.assertIsInstance(obj_dict, dict)

        self.assertEqual(obj_dict['__class__'], 'BaseModel')
        self.assertEqual(obj_dict['id'], my_model.id)
        self.assertEqual(obj_dict['created_at'], my_model.created_at.isoformat())
        self.assertEqual(obj_dict['updated_at'], my_model.updated_at.isoformat())
        self.assertTrue('save' in obj_dict)

    def testString(self):
        my_model = BaseModel()

        self.assertTrue(str(my_model).startswith('[BaseModel]'))
        self.assertIn(str(my_model.id), str(my_model))
        self.assertIn(str(my_model.__dict__), str(my_model))


if __name__ == "__main__":
    unittest.main()
