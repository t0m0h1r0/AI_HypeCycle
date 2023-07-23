import os
import argparse


class TextProcessor:
    def __init__(self, input_file_path, intro_file_path, output_dir, output_file_prefix):
        self.input_file_path = input_file_path
        self.intro_file_path = intro_file_path
        self.output_dir = output_dir
        self.output_file_prefix = output_file_prefix

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return [line.rstrip() for line in file]

    @staticmethod
    def write_file(file_path, content):
        with open(file_path, 'w') as file:
            file.writelines(content)

    def get_intro_text(self):
        return self.read_file(self.intro_file_path)

    @staticmethod
    def divide_text_into_sections(lines):
        sections = []
        section_lines = []

        for i, line in enumerate(lines):
            if line.startswith("Analysis By"):
                if section_lines:
                    sections.append('\n'.join(section_lines[:-1]) + '\n')
                section_lines = [lines[i - 1]] if i > 0 else []
            section_lines.append(line)

        if section_lines:
            sections.append('\n'.join(section_lines) + '\n')

        return sections

    def add_intro_text_to_each_section(self, sections):
        intro_text_lines = [line for line in self.get_intro_text() if line != "'''"]

        for i, section in enumerate(sections):
            sections[i] = '\n'.join(intro_text_lines) + '\n' + section

        return sections

    def write_sections_to_separate_files(self, sections):
        for i, section in enumerate(sections, start=1):
            output_file_path = os.path.join(self.output_dir, f"{self.output_file_prefix}_{i}.txt")
            self.write_file(output_file_path, section)

    def process_text(self):
        lines = self.read_file(self.input_file_path)
        sections = self.divide_text_into_sections(lines)
        sections_with_intro = self.add_intro_text_to_each_section(sections)
        self.write_sections_to_separate_files(sections_with_intro)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--input_file', required=True, help='Path to the input file')
    parser.add_argument('--intro_file', required=True, help='Path to the intro file')
    parser.add_argument('--output_dir', default='./', help='Output directory')
    parser.add_argument('--output_file_prefix', default='section', help='Prefix for the output file names')

    return parser.parse_args()


def main():
    args = parse_arguments()

    processor = TextProcessor(args.input_file, args.intro_file, args.output_dir, args.output_file_prefix)
    processor.process_text()


if __name__ == "__main__":
    main()
