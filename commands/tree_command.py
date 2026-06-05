import os


class TreeCommand:

    def execute(self, args):

        path = "."
        dirs_only = False
        files_only = False
        max_depth = None

        i = 0

        while i < len(args):

            if args[i] == "-d":
                dirs_only = True

            elif args[i] == "-f":
                files_only = True

            elif args[i] == "-L":

                if i + 1 >= len(args):
                    print("Usage: tree -L <depth>")
                    return

                max_depth = int(args[i + 1])
                i += 1

            else:
                path = args[i]

            i += 1

        print(os.path.basename(os.path.abspath(path)))

        self.print_tree(
            path,
            dirs_only=dirs_only,
            files_only=files_only,
            max_depth=max_depth
        )

    def print_tree(
        self,
        base,
        prefix="",
        depth=1,
        dirs_only=False,
        files_only=False,
        max_depth=None
    ):

        if max_depth is not None and depth > max_depth:
            return

        try:
            entries = sorted(os.listdir(base))

        except Exception as e:
            print(prefix + f"Error: {e}")
            return

        filtered = []

        for entry in entries:

            full_path = os.path.join(base, entry)

            if dirs_only and not os.path.isdir(full_path):
                continue

            if files_only and not os.path.isfile(full_path):
                continue

            filtered.append(entry)

        for index, entry in enumerate(filtered):

            full_path = os.path.join(base, entry)

            is_last = index == len(filtered) - 1

            connector = "└── " if is_last else "├── "

            print(prefix + connector + entry)

            if os.path.isdir(full_path):

                extension = (
                    "    "
                    if is_last
                    else "│   "
                )

                self.print_tree(
                    full_path,
                    prefix + extension,
                    depth + 1,
                    dirs_only,
                    files_only,
                    max_depth
                )