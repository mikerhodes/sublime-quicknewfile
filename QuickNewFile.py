import os

import sublime
import sublime_plugin

class QuickNewFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.setup()
        self.show_filename_input()

    def setup(self):
        self.view = self.window.active_view()

    @property
    def input_panel_caption(self):
        """Just the caption for the input panel"""
        return "Filename:"

    def show_filename_input(self):
        """Show the input panel for the user to enter the file to open/create"""
        self.input_panel_view = self.window.show_input_panel(
            self.input_panel_caption,
            self.initial_directory(),
            self.on_done, self.on_edit, self.on_cancel
        )

    def initial_directory(self):
        """Get the directory for the currently open file, then project."""
        if self.view.file_name():
            directory, _ = os.path.split(self.view.file_name())
            return directory + os.sep

        project_folders = window.project_data()['folders']
        if project_folders:
            return project_folders[0]['path'] + os.sep

        # This can kill ST for folders which have many subfolders (e.g., ~).
        # So we avoid it for now.
        # folders = self.window.folders()
        # if folders:
        #     return folders[0] + os.sep

        # Fall back to home (TODO: does this work outside of OS X?)
        return os.path.expanduser('~') + os.sep

    def on_done(self, input_string):
        """Called when input dialog is done (i.e., action should happen)

        Will open the file specified by input string, creating directories
        and files which are required to do so.

        """
        if len(input_string) == 0:
            self.show_error("Empty input")
            return

        directory, fname = os.path.split(input_string)
        if os.path.exists(directory) and not os.path.isdir(directory):
            self.show_error("Directory path exists, but isn't a directory")
            return

        if len(fname) == 0:
            self.show_error("Empty filename")
            return

        self.ensure_directory_exists(directory)
        self.ensure_file_exists(os.path.join(directory, fname))

        self.window.open_file(os.path.join(directory, fname))

    def on_edit(self, input_string):
        """Called when input dialog is edited

        TODO: at some point can we do folder complete here?
        """
        pass

    def on_cancel(self):
        """Called when input dialog is cancelled.

        We need to do nothing here.
        """
        pass

    def show_error(self, msg):
        """Shows an error message to the user"""
        sublime.status_message("[QuickNewFile] Error: {0}".format(msg))

    def ensure_file_exists(self, path):
        """Simply make sure a file exists at `path` to be opened"""
        open(path, "a").close()

    def ensure_directory_exists(self, path):
        """Create a directory, and required parent directies, if needed"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise

