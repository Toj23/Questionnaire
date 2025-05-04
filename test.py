import unittest 
from unittest.mock import patch 
import os
import json
import questionnaire
import questionnaire_import



class TestsQuestion(unittest.TestCase):
    def test_bonne_mauvaise_reponse(self):
        choix = ("choix1","choix2", "choix3")
        q = questionnaire.Question("titre_question",choix,"choix2")
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser(1, 1))
        with patch("builtins.input", return_value="2"):
            self.assertTrue(q.poser(1, 1))
        with patch("builtins.input", return_value="3"):
            self.assertFalse(q.poser(1, 1))
        
class TestsQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_alien_debutant(self):
        filename = os.path.join("Section_72", "mission", "Questionnaire", "test_data", "cinema_alien_debutant.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(len(q.questions), 10)
        self.assertEqual(q.titre, "Alien")
        self.assertEqual(q.categorie, "Cinéma")
        self.assertEqual(q.difficulte, "débutant")
        with patch("builtins.input", return_value="1"):
            self.assertEqual(q.lancer(), 1)
    
    
class TestsImportQuestionnaire(unittest.TestCase):
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json")
        filenames = ("animaux_leschats_confirme.json","animaux_leschats_debutant.json","animaux_leschats_expert.json")
        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            try:
                data = json.loads(json_data)
            except:
                self.fail("Problème de décérialisation pour le fichier" + filename)
                
            self.assertIsNotNone(data.get("titre"))
            self.assertIsNotNone(data.get("questions"))
            self.assertIsNotNone(data.get("difficulte"))
            self.assertIsNotNone(data.get("categorie"))

            for question in data.get("questions"):
                self.assertIsNotNone(question.get("titre"))
                self.assertIsNotNone(question.get("choix"))
                for choix in question.get("choix"):
                    self.assertGreater(len(choix[0]), 0)
                    self.assertTrue(isinstance(choix[1] , bool))
                bonne_reponse = [i for i in question.get("choix") if i[1]]
                self.assertEqual(len(bonne_reponse), 1)
                
unittest.main() 