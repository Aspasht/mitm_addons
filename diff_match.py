from diff_match_patch import diff_match_patch

class HTMLComparer:
    def __init__(self, file_path1, file_path2):
        self.file_path1 = file_path1
        self.file_path2 = file_path2
    
    def compare_and_extract_changes(self):
        with open(self.file_path1, 'r', encoding='utf-8') as file1:
            content1 = file1.read()

        with open(self.file_path2, 'r', encoding='utf-8') as file2:
            content2 = file2.read()

        dmp = diff_match_patch()
        diffs = dmp.diff_main(content1, content2)
        dmp.diff_cleanupSemantic(diffs)

        changes = [line for op, line in diffs if op == dmp.DIFF_INSERT or op == dmp.DIFF_DELETE]
        return changes
