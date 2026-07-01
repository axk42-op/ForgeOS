"""Virtual filesystem for Forge OS."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


class VFSError(Exception):
    """Virtual filesystem error."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


@dataclass
class VFSNode:
    """A node in the virtual filesystem tree."""

    name: str
    is_dir: bool = False
    content: str = ""
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    children: dict[str, "VFSNode"] = field(default_factory=dict)

    def touch(self) -> None:
        self.modified = datetime.now(timezone.utc)


class VirtualFileSystem:
    """In-memory virtual filesystem."""

    def __init__(self) -> None:
        self._root = VFSNode(name="/", is_dir=True)
        self._initialize_default_tree()

    def _initialize_default_tree(self) -> None:
        self._mkdir_abs("/home")
        self._mkdir_abs("/home/forge")
        self._mkdir_abs("/bin")
        self._mkdir_abs("/usr")
        self._mkdir_abs("/usr/bin")
        self._mkdir_abs("/etc")
        self._mkdir_abs("/var")
        self._mkdir_abs("/tmp")
        self._write_file("/etc/hosts", "127.0.0.1 localhost\n")
        self._write_file("/etc/forge-release", "Forge OS 2.0.0\n")
        self._write_file(
            "/etc/LICENSE",
            "Forge OS — MIT License\n\nCopyright (c) 2026 Forge OS Contributors\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy "
            "of this software and associated documentation files (the \"Software\"), to deal "
            "in the Software without restriction, including without limitation the rights "
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
            "copies of the Software, and to permit persons to whom the Software is "
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all "
            "copies or substantial portions of the Software.\n",
        )
        self._write_file(
            "/home/forge/.bashrc",
            "# Forge Shell configuration\n# Placeholder\n",
        )

    def ensure_user_home(self, username: str) -> str:
        """Create /home/<username> if it does not exist."""
        home_path = f"/home/{username}"
        self._mkdir_abs("/home")
        if not self.exists(home_path):
            self._mkdir_abs(home_path)
            self._write_file(
                f"{home_path}/.bashrc",
                f"# Forge Shell configuration for {username}\n",
            )
        return home_path

    def resolve(self, path: str, cwd: str = "/") -> str:
        if path.startswith("/"):
            base = path
        else:
            base = self._join(cwd, path)

        parts = [part for part in base.split("/") if part and part != "."]
        stack: list[str] = []
        for part in parts:
            if part == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(part)
        return "/" + "/".join(stack) if stack else "/"

    def exists(self, path: str, cwd: str = "/") -> bool:
        try:
            self._get_node(path, cwd)
            return True
        except VFSError:
            return False

    def is_dir(self, path: str, cwd: str = "/") -> bool:
        try:
            node = self._get_node(path, cwd)
            return node.is_dir
        except VFSError:
            return False

    def is_file(self, path: str, cwd: str = "/") -> bool:
        node = self._get_node(path, cwd)
        return not node.is_dir

    def list_dir(self, path: str = ".", cwd: str = "/") -> list[VFSNode]:
        node = self._get_node(path, cwd)
        if not node.is_dir:
            raise VFSError(f"not a directory: {self.resolve(path, cwd)}")
        return sorted(node.children.values(), key=lambda n: (not n.is_dir, n.name))

    def read_file(self, path: str, cwd: str = "/") -> str:
        node = self._get_node(path, cwd)
        if node.is_dir:
            raise VFSError(f"is a directory: {self.resolve(path, cwd)}")
        return node.content

    def write_file(self, path: str, content: str = "", cwd: str = "/") -> str:
        resolved = self.resolve(path, cwd)
        return self._write_file(resolved, content)

    def mkdir(self, path: str, cwd: str = "/", parents: bool = False) -> str:
        resolved = self.resolve(path, cwd)
        if self.exists(resolved):
            raise VFSError(f"already exists: {resolved}")

        parts = [part for part in resolved.split("/") if part]
        current = self._root
        built: list[str] = []

        for part in parts[:-1]:
            built.append(part)
            if part not in current.children:
                if not parents:
                    raise VFSError(f"no such directory: {'/' + '/'.join(built)}")
                current.children[part] = VFSNode(name=part, is_dir=True)
            child = current.children[part]
            if not child.is_dir:
                raise VFSError(f"not a directory: {'/' + '/'.join(built)}")
            current = child

        leaf = parts[-1] if parts else ""
        if leaf:
            current.children[leaf] = VFSNode(name=leaf, is_dir=True)
        return resolved

    def touch(self, path: str, cwd: str = "/") -> str:
        resolved = self.resolve(path, cwd)
        if self.exists(resolved):
            node = self._get_node(resolved)
            node.touch()
            return resolved
        return self._write_file(resolved, "")

    def remove(self, path: str, cwd: str = "/", recursive: bool = False) -> str:
        resolved = self.resolve(path, cwd)
        if resolved == "/":
            raise VFSError("cannot remove root directory")

        parent_path, name = self._split_parent(resolved)
        parent = self._get_node(parent_path)
        if name not in parent.children:
            raise VFSError(f"no such file or directory: {resolved}")

        node = parent.children[name]
        if node.is_dir and node.children and not recursive:
            raise VFSError(f"directory not empty: {resolved}")

        del parent.children[name]
        return resolved

    def copy(self, source: str, dest: str, cwd: str = "/") -> tuple[str, str]:
        src_resolved = self.resolve(source, cwd)
        dst_resolved = self.resolve(dest, cwd)
        node = self._get_node(src_resolved)

        if node.is_dir:
            raise VFSError(f"directory copy not supported: {src_resolved}")

        return src_resolved, self._write_file(dst_resolved, node.content)

    def move(self, source: str, dest: str, cwd: str = "/") -> tuple[str, str]:
        src_resolved = self.resolve(source, cwd)
        dst_resolved = self.resolve(dest, cwd)
        node = self._get_node(src_resolved)

        if node.is_dir:
            raise VFSError(f"directory move not supported: {src_resolved}")

        content = node.content
        destination = self._write_file(dst_resolved, content)
        self.remove(src_resolved)
        return src_resolved, destination

    def find(self, pattern: str, path: str = ".", cwd: str = "/") -> list[str]:
        root = self.resolve(path, cwd)
        matches: list[str] = []

        def walk(current_path: str, node: VFSNode) -> None:
            full_path = current_path if current_path != "/" else f"/{node.name}" if node.name != "/" else "/"
            if node.name != "/" and self._matches(pattern, node.name):
                matches.append(full_path)
            if node.is_dir:
                for child in node.children.values():
                    child_path = f"{full_path}/{child.name}" if full_path != "/" else f"/{child.name}"
                    walk(child_path, child)

        start = self._get_node(root)
        if start.name == "/":
            for child in start.children.values():
                walk(f"/{child.name}", child)
        else:
            walk(root, start)
        return sorted(matches)

    def tree(self, path: str = ".", cwd: str = "/") -> list[str]:
        resolved = self.resolve(path, cwd)
        node = self._get_node(resolved)
        lines: list[str] = [resolved if resolved != "/" else "/"]

        def walk(prefix: str, current: VFSNode, is_last: bool) -> None:
            children = sorted(current.children.values(), key=lambda n: n.name)
            for index, child in enumerate(children):
                last = index == len(children) - 1
                connector = "└── " if last else "├── "
                suffix = "/" if child.is_dir else ""
                lines.append(f"{prefix}{connector}{child.name}{suffix}")
                if child.is_dir:
                    extension = "    " if last else "│   "
                    walk(prefix + extension, child, last)

        if node.is_dir:
            walk("", node, True)
        return lines

    def _write_file(self, resolved: str, content: str) -> str:
        parent_path, name = self._split_parent(resolved)
        if not name:
            raise VFSError("invalid path")

        parent = self._get_node(parent_path)
        if not parent.is_dir:
            raise VFSError(f"not a directory: {parent_path}")

        if name in parent.children and parent.children[name].is_dir:
            raise VFSError(f"is a directory: {resolved}")

        if name in parent.children:
            file_node = parent.children[name]
            file_node.content = content
            file_node.touch()
        else:
            parent.children[name] = VFSNode(name=name, is_dir=False, content=content)
        return resolved

    def _mkdir_abs(self, path: str) -> VFSNode:
        resolved = self.resolve(path)
        parts = [part for part in resolved.split("/") if part]
        current = self._root
        for part in parts:
            if part not in current.children:
                current.children[part] = VFSNode(name=part, is_dir=True)
            current = current.children[part]
        return current

    def _get_node(self, path: str, cwd: str = "/") -> VFSNode:
        resolved = self.resolve(path, cwd)
        if resolved == "/":
            return self._root

        parts = [part for part in resolved.split("/") if part]
        current = self._root
        for part in parts:
            if part not in current.children:
                raise VFSError(f"no such file or directory: {resolved}")
            current = current.children[part]
        return current

    def _split_parent(self, path: str) -> tuple[str, str]:
        if path == "/":
            return "/", ""
        parent, _, name = path.rpartition("/")
        return parent or "/", name

    def _join(self, base: str, relative: str) -> str:
        if relative.startswith("/"):
            return relative
        if base.endswith("/"):
            return base + relative
        return base + "/" + relative

    @staticmethod
    def _matches(pattern: str, name: str) -> bool:
        if pattern == "*":
            return True
        if pattern.startswith("*") and name.endswith(pattern[1:]):
            return True
        return pattern in name
