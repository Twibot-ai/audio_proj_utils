class Help:
    def call(self):
        print(self.message())

    def message(self):
        lines = [
            "Usage: python main.py <action name> <arguments>",
            "Available actions: create_dataset, help, separate",
            "For generating dataset it is REQUIRED to install ffmpeg, ffprobe and add them to environment",
            "Be sure to use quotes for path or any other with spaces. For example: 'F://pony/without panties/'"
        ]
        return '\n'.join(lines)
