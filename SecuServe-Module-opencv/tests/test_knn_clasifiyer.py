""" 
this file is for testing the datasturue for handing faces
#author Nicholas 
To make tests think about black box reverse enginnering only what inputs and what out puts are required/ expected
"""
import unittest
from pipeline import knnClasifiyer as knn
from util import const as config


class TestKnnClass(unittest.TestCase):
    """

    This is for only testing if kkn clasifiyer is none
    """

    def test_training_knn_clasifiyer(self):
        data = knn.train(
            train_dir=config.TEST_TRAIN_DIR,
            model_save_path=config.TEST_TRAIN_DIR + "test.model",
            n_neighbors=2,
        )
        self.assertIsNone(data)

    # this will test trained test knn classifiyer aginst a known image UwU

    def test_read_knn_classifiyer(self):

        predict = knn.predict(
            config.READIMAGE,
            knn_clf=knn.loadTrainedModel(
                knn_clf=None, model_path=config.TEST_TRAIN_DIR + "test.model"
            ),
            distance_threshold=0.65,
        )
        self.assertEqual(predict, [("me", (145, 312, 287, 170))])
