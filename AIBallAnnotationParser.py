import os

class AIBallAnnotationParser:

    def __init__(self, dir_path):
        self.export_file_id = "export"
        sub_dir_list = os.listdir(dir_path)

        for item in sub_dir_list:
            if self.export_file_id in item:
                self.file_path = os.path.join(dir_path, item)
                print("found annotations file: {}".format(self.file_path))
                break

        assert self.file_path is not None

    def read_ai_ball_file(self):
        annotations = dict()

        with open(self.file_path, 'r') as fp:
            lines = fp.read().splitlines()

            format_columns = None

            for i, line in enumerate(lines):

                if '[format: "' in line:
                    format_columns = self.parse_format(line)
                    continue

                if format_columns is None:
                    continue

                if line is "":
                    continue

                filename, annotation = self.parse_annotation(format_columns, line)

                if annotation is not None:
                    annotations[filename] = annotation

        return annotations

    def parse_format(self, line):
        tmp1 = line.split('[format: "')
        tmp2 = tmp1[1].split('"]')
        columns = tmp2[0].split('|')
        print('found columns: {}'.format(columns))
        return columns

    def parse_annotation(self, format_columns, line):
        tokens = line.split('|')

        annotation = dict()

        if len(tokens) != len(format_columns):
            assert 'not_in_image' in line
            filename_index = format_columns.index("filename")
            annotation['filename'] = tokens[filename_index]
            return annotation['filename'], annotation

        for i, column in enumerate(format_columns):
            annotation[column] = tokens[i]

        return annotation['filename'], annotation
