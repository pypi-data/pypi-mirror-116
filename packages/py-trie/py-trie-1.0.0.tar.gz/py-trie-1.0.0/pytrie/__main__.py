import sys
import click
import requests
import unittest
from tests import test as trie_test

SERVER = "https://trie-container-xuuikixata-uc.a.run.app/"

def send_request(word, method, request_type):
    if word != '__None__' and not word.isalpha():
        click.echo("Please enter a valid word containing only letters.")
        return
    if len(word) > 950:
        click.echo("Please enter a valid word containing only letters that is less than 950 characters.")
        return
    api = SERVER + method
    if word == '__None__':
        data = None
    else:
        data = {"word": word.lower()}
    if request_type == 'POST':
        response = requests.post(api, json=data)
    elif request_type == 'GET':
        response = requests.get(api, params=data)
    click.echo(response.text)
    return

@click.group()
@click.version_option("1.0.0")
def main():
    """Py-Trie CLI"""
    pass

@main.command()
@click.argument('word', required=True)
def insert(word):
    """Insert word to trie"""
    send_request(word, 'insert', 'POST')

@main.command()
@click.argument('word', required=True)
def search(word):
    """Search for word in trie"""
    send_request(word, 'search', 'GET')

@main.command()
@click.argument('word', required=True)
def remove(word):
    """Remove word from trie"""
    send_request(word, 'delete', 'POST')

@main.command()
@click.argument('prefix', required=True)
def autocomplete(prefix):
    """Returns list of existing words in trie based on prefix"""
    send_request(prefix, 'autocomplete', 'GET')

@main.command()
def display():
    """Display words in trie"""
    send_request('__None__', 'display', 'GET')

@main.command()
def test():
    """Runs test cases"""
    test_suite = unittest.TestLoader().loadTestsFromModule(trie_test)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == '__main__':
    args = sys.argv
    main()
