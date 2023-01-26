from sfm.types import Group, ManagedDir

TEST_PARSED_MANAGED_DIRS = {
    'managed_dir_A': ManagedDir(
        base_dir='/work/tests/example_directory_a',
        groups={
            'group_A': Group(
                path='group_A_name',
                keywords=['keyword_A', 'keyword_B'],
            ),
            'group_C': Group(
                path='some_subdir/group_C',
                keywords=['keyword_C']
            ),
        }
    ),
    'managed_dir_B': ManagedDir(
        base_dir='/work/tests/example_directory_b',
        groups={
            'group_A': Group(
                path='group_A_name',
                keywords=['keyword_A', 'keyword_B'],
            )
        }
    )
}
