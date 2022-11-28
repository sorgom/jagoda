# VS Code Memos

### Case changing in regex replace

VS Code now supports changing the case of regex matching groups while doing a find/replace in the editor. This is done with the modifiers `\u\U\l\L`, where `\u` and `\l` will upper/lowercase a single character, and `\U` and `\L` will upper/lowercase the rest of the matching group.

Example:

[![Changing case while doing find and replace](https://github.com/microsoft/vscode-docs/raw/vnext/release-notes/images/1_47/case-change-replace.gif)](https://github.com/microsoft/vscode-docs/blob/vnext/release-notes/images/1_47/case-change-replace.gif)

The modifiers can also be stacked - for example, `\u\u\u$1` will uppercase the first three characters of the group, or `\l\U$1` will lowercase the first character, and uppercase the rest.
