import importlib
import subprocess

from clint.textui import colored, puts
from pyfiglet import Figlet
from PyInquirer import prompt

from styles import style


class YsTester:

    def __init__(self):
        self.figlet = Figlet(font='slant')
        self.print_figlet("Yo Tester!")

    def print_figlet(self, text: str) -> None:
        puts(colored.green(self.figlet.renderText(text)))

    def select_option(self):
        options = [
            {
                'type': 'list',
                'name': 'choice',
                'message': "Please select any test module:",
                'choices': [
                    'Sort Imports',
                    'Unit Test',
                    # Separator(),
                    'Code Coverage',
                    'Code Complexity',
                    'Bandit (Security Test)',
                    'Check Code Formatting',
                    'Check Code Duplication',
                    'Quit'
                ]
            }
        ]
        response = prompt(options, style=style)
        choice = response.get('choice').lower().replace(" ", "-")

        if choice == "sort-imports":
            self.sort_imports()
        elif choice == "unit-test":
            self.run_unit_test()
        elif choice == "code-coverage":
            pass
        elif choice == "code-complexity":
            pass
        elif choice == "bandit-(security-test)":
            pass
        elif choice == "check-code-formatting":
            pass
        elif choice == "check-code-duplication":
            pass

        self.print_figlet("Good Bye!")

    def sort_imports(self) -> None:
        if importlib.util.find_spec('isort') is None:
            puts(colored.red("isort not found, installing it now.\n"))

            process = subprocess.Popen(
                ['pip', 'install', 'isort'], stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                print(output.strip().decode('utf-8'))

            process.poll()

        puts(colored.cyan("\nisort your imports, so you don't have to."))
        puts(colored.cyan("Visit official url: "), newline=False)
        puts(colored.green("https://pycqa.github.io/isort/\n"))

        questions = [
            {
                'type': 'input',
                'name': 'source',
                'message': "Scan Directory [.]",
                'default': '.'
            },
        ]

        answers = prompt(questions)
        source = answers.get('source')

        puts(colored.cyan("\nRunning isort on {}\n".format(source)))

        command = ['python', '-m', 'isort']
        if source is not '.':
            command = ['python', '-m', 'isort', source]

        process = subprocess.Popen(command, stdout=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            print(output.strip().decode('utf-8'))

        process.poll()

    def run_unit_test(self) -> None:
        puts(colored.cyan("The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries."))
        puts(colored.cyan("Visit official url: "), newline=False)
        puts(colored.green("https://docs.pytest.org/en/latest/"))

    def run_seciruty_check(self) -> None:
        pass

    def check_code_formatting(self) -> None:
        pass

    def check_code_duplication(self) -> None:
        pass
