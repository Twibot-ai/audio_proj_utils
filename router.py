class Router:
    def __init__(self, action, *args):
        if action == 'help':
            from commands.help import Help
            Help().call()
        elif action == 'create_dataset':
            from commands.create_dataset import CreateDataset
            CreateDataset(*args).call()
        elif action == 'separate':
            from commands.separate import SeparatePony
            SeparatePony(*args).call()
        else:
            print('Your action was not found')
