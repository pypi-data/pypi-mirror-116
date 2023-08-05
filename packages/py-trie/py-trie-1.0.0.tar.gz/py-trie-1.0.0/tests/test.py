import unittest
import requests
import json
import threading

class TestTrie(unittest.TestCase):

    def send_request(self, word, method, request_type):
        if word != "__None__" and not word.isalpha():
            return "Please enter a valid word containing only letters."
        if len(word) >= 950:
            return "Please enter a valid word containing only letters that is less than 950 characters."
        api = "https://trie-container-xuuikixata-uc.a.run.app/" + method
        if word == "__None__":
            data = None
        else:
            data = {"word": word.lower()}
        if request_type == 'POST':
            response = requests.post(api, json=data)
        elif request_type == 'GET':
            response = requests.get(api, params=data)
        return response.text

    def compareLists(self, response, expected_response):
        return all(word in response for word in expected_response)

    ########## Testing Insertion Function ##########

    def test_insert(self):
        self.send_request("test", 'insert', 'POST')
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertIn("test", words, "\"test\" should be in words list")

    def test_insert_numbers(self):
        message = self.send_request("abc123", 'insert', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("abc123", words, "\"abc123\" should not be in words list")

    def test_insert_special_character(self):
        message = self.send_request("a@b!c_d+.", 'insert', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("a@b!c_d+.", words, "\"a@b!c_d+.\" should not be in words list")

    def test_insert_empty_string(self):
        message = self.send_request("", 'insert', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("", words, "\"\" should not be in words list")
    
    def test_insert_single_quote(self):
        message = self.send_request("Steven's", 'insert', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("Steven's", words, "\"\" should not be in words list")

    def test_insert_long_word(self):
        message = self.send_request("a" * 950, 'insert', 'POST')
        self.assertEqual("Please enter a valid word containing only letters that is less than 950 characters.", message, "Should be \"Please enter a valid word containing only letters that is less than 950 characters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("a" * 950, words, "\"a...\" should not be in words list")
        
    def test_insert_threading(self):

        # Ensure "pizza" is not in trie
        self.send_request("pizza", 'delete', 'POST')

        # Simulate different user trying to insert same word
        def thread_insert():
            thread_response = self.send_request("pizza", 'insert', 'POST')
            self.assertEqual("Word already exists", thread_response, "Should be \"Word already exists\"")

        thread = threading.Thread(target=thread_insert)
        response = self.send_request("pizza", 'insert', 'POST')
        thread.start()
        self.assertEqual("Successful Entry!", response, "Should be \"Successful Entry!\"")
        thread.join()
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertIn("pizza", words, "\"pizza\" should not be in words list")

    ########## Testing Deletion Function ##########

    def test_delete(self):
        self.send_request("car", 'delete', 'POST')
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("car", words, "\"car\" should not be in words list")

    def test_delete_numbers(self):
        message = self.send_request("abc123", 'delete', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("abc123", words, "\"abc123\" should not be in words list")

    def test_delete_special_character(self):
        message = self.send_request("a@b!c_d+.", 'delete', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("a@b!c_d+.", words, "\"a@b!c_d+.\" should not be in words list")

    def test_delete_empty_string(self):
        message = self.send_request("", 'delete', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("", words, "\"\" should not be in words list")

    def test_delete_single_quote(self):
        message = self.send_request("Steven's", 'delete', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("Steven's", words, "\"\" should not be in words list")

    def test_delete_long_word(self):
        message = self.send_request("a" * 950, 'delete', 'POST')
        self.assertEqual("Please enter a valid word containing only letters that is less than 950 characters.", message, "Should be \"Please enter a valid word containing only letters that is less than 950 characters.\"")
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("a" * 950, words, "\"a...\" should not be in words list")

    def test_delete_threading(self):

        # Ensure "pasta" is in trie
        self.send_request("pasta", 'insert', 'POST')

        # Simulate different user trying to insert same word
        def thread_delete():
            thread_response = self.send_request("pasta", 'delete', 'POST')
            self.assertEqual("Word not found", thread_response, "Should be \"Word not found\"")

        thread = threading.Thread(target=thread_delete)
        response = self.send_request("pasta", 'delete', 'POST')
        thread.start()
        self.assertEqual("Successful Deletion!", response, "Should be \"Successful Deletion!\"")
        thread.join()
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("pasta", words, "\"pasta\" should not be in words list")
    
    ########## Testing Search Function ##########

    def test_search(self):
        self.send_request("balloon", 'insert', 'POST')
        response = self.send_request("balloon", 'search', 'GET')
        self.assertEqual("True, word found!", response, "Should be \"True, word found!\"")
        self.send_request("balloon", 'delete', 'POST')
        response = self.send_request("balloon", 'search', 'GET')
        self.assertEqual("False, word does not exist!", response, "Should be \"False, word does not exist!\"")
    
    def test_search_numbers(self):
        message = self.send_request("abc123", 'search', 'GET')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")
        
    def test_search_special_character(self):
        message = self.send_request("a@b!c_d+.", 'search', 'GET')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")

    def test_search_empty_string(self):
        message = self.send_request("", 'search', 'POST')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")

    def test_search_single_quote(self):
        message = self.send_request("Steven's", 'search', 'GET')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")

    def test_search_long_word(self):
        message = self.send_request("a" * 950, 'search', 'GET')
        self.assertEqual("Please enter a valid word containing only letters that is less than 950 characters.", message, "Should be \"Please enter a valid word containing only letters that is less than 950 characters.\"")
        
    ########## Testing Autocomplete Function ##########

    def test_autocomplete_1(self):
        self.send_request("pizza", 'insert', 'POST')
        self.send_request("pisa", 'insert', 'POST')
        self.send_request("pasta", 'insert', 'POST')
        response = self.send_request("pi", 'autocomplete', 'GET')
        self.assertTrue(self.compareLists(response, ["pizza", "pisa"]))

    def test_autocomplete_2(self):
        self.send_request("pizza", 'insert', 'POST')
        self.send_request("pisa", 'insert', 'POST')
        self.send_request("pasta", 'insert', 'POST')
        response = self.send_request("pizza", 'autocomplete', 'GET')
        self.assertTrue(self.compareLists(response, ["pizza"]))

    def test_autocomplete_3(self):
        self.send_request("pizza", 'insert', 'POST')
        self.send_request("pisa", 'insert', 'POST')
        self.send_request("pasta", 'insert', 'POST')
        response = self.send_request("pizzas", 'autocomplete', 'GET')
        self.assertEqual("No matching words", response, "Should be \"No matching words\"")

    def test_autocomplete_special_character(self):
        message = self.send_request("a@", 'autocomplete', 'GET')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")

    def test_autocomplete_empty_string(self):
        message = self.send_request("", 'autocomplete', 'GET')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")

    def test_autocomplete_single_quote(self):
        message = self.send_request("'s", 'autocomplete', 'GET')
        self.assertEqual("Please enter a valid word containing only letters.", message, "Should be \"Please enter a valid word containing only letters.\"")

    def test_autocomplete_long_word(self):
        message = self.send_request("a" * 950, 'autocomplete', 'GET')
        self.assertEqual("Please enter a valid word containing only letters that is less than 950 characters.", message, "Should be \"Please enter a valid word containing only letters that is less than 950 characters.\"")
    
    ########## Testing Global State ##########

    def test_global_state_1(self):

        # Ensure "plaza" is not in trie
        self.send_request("plaza", 'delete', 'POST')

        # Simulate different user trying to delete word that was inserted by different user
        def thread_insert():
            thread_response = self.send_request("plaza", 'delete', 'POST')
            self.assertEqual("Successful Deletion!", thread_response, "Should be \"Successful Deletion!\"")

        thread = threading.Thread(target=thread_insert)
        
        # One user inserts word
        response = self.send_request("plaza", 'insert', 'POST')
        thread.start()
        self.assertEqual("Successful Entry!", response, "Should be \"Successful Entry!\"")
        thread.join()
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertNotIn("plaza", words, "\"plaza\" should not be in words list")

    def test_global_state_2(self):

        # Ensure "plaza" and "school" are not in trie
        self.send_request("school", 'delete', 'POST')
        self.send_request("park", 'delete', 'POST')

        # Simulate different user trying to delete word that was inserted by different user
        def thread_insert():
            thread_response = self.send_request("park", 'insert', 'POST')
            self.assertEqual("Successful Entry!", thread_response, "Should be \"Successful Entry!\"")

        thread = threading.Thread(target=thread_insert)
        
        # One user inserts word
        response = self.send_request("school", 'insert', 'POST')
        thread.start()
        self.assertEqual("Successful Entry!", response, "Should be \"Successful Entry!\"")
        thread.join()
        words = json.loads(self.send_request("__None__", 'display', 'GET'))
        self.assertTrue(self.compareLists(words, ["school", "park"]))

if __name__ == "__main__":
    unittest.main()
