import difflib

class HTMLComparer:
    def __init__(self, file_path1, file_path2):
        self.file_path1 = file_path1
        self.file_path2 = file_path2
    
    def compare_and_extract_changes(self):
        with open(self.file_path1, 'r', encoding='utf-8') as file1:
            content1 = file1.readlines()

        with open(self.file_path2, 'r', encoding='utf-8') as file2:
            content2 = file2.readlines()

        differ = difflib.Differ()
        diff = list(differ.compare(content1, content2))

        changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
        return changes
