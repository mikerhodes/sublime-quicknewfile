# Sublime QuickNewFile

This is a small Sublime Text plugin which mimics Atom's new file funtion. Instead of opening a blank file, it displays an input initialised with the current file's directory (if no files are open, it'll try to figure a directory to use). Add a filename and you're good to go.

![QuickNewFile](QuickNewFile.png)

## Install

Install by cloning this repository into your Sublime Text packages folder:

- OS X: `~/Library/Application Support/Sublime Text 3/Packages`
- Windows: `%APPDATA%\Sublime Text 3\Packages`
- Linux: `~/.config/sublime-text-3/Packages`

## Using

The default hotkey is `super-alt-n`, where `super` is the `win` or `cmd` keys.

These also an entry in the File menu.

## Why

This fits with my use of new file better -- enter the name first, rather than the content. It also is a bit smarter about where to put the file than Sublime's normal File - New, which seems a bit random in its choices.

It's also a little different from [Sublime-AdvancedNewFile](https://github.com/skuroda/Sublime-AdvancedNewFile) in that it does a single thing, hopefully well. Certainly if this plugin doesn't fit your needs, look to Sublime-AdvancedNewFile.
