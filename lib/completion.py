import os

import sublime

STATE_NOT_COMPLETING = 0
STATE_COMPLETING = 1

class CompletionStateMachine(object):
    """This class maintains a state machine for path-based tab completion.

                        tab
         ----    ------------------    ------
        |    |  |                  v  |      |
    not |    not               competing     | tab
    tab |    completing            |  ^      |
        |    ^  ^                  |  |      |
        |    |  |                  |  |      |
         ----    ------------------    ------
                        not tab

    Calling `transition` with a string will look at the last character of the
    string and perform the appropriate transition. `transition` should
    therefore be called after every user key press but not when making an
    automatic update based on a completion (otherwise you'll transition out
    which will break the cycling of completions).

    When in the completing state, calling `complete` will return a completion
    for the prefix path that was used when transitioning into the completing
    state. Repeatedly calling complete while in the completing state will
    return subsequent possible completions for the prefix path.

    On calling transition with a string not ending in tab, the state will
    return to not completing and calling complete will do nothing.

    The initial state is not completing.

    The idea is you call `transition` then `complete` after every key press --
    the class will handle the details of whether a completion should be
    returned at this point automatically, you can rely on it returning
    None from `complete` when not in the completion state rather than checking
    the state itself.
    """

    def __init__(self):
        # State we're currently in
        self.state = STATE_NOT_COMPLETING

        # This stores the 'root' for the completion, the value we see
        # when tab is pressed. Keeping hold of this allows completion
        # after we change the value of the input field.
        self.completion_base = None

        # Store the last folder name we used for completion so we can
        # loop through completions as the users hits tab repeatedly.
        self.previous_completion = None

    def transition(self, buffer_content):
        """Simple transitions:

        - if in STATE_NOT_COMPLETING and user hits tab, move to STATE_COMPLETING
        - when in STATE_COMPLETING, hitting anything but tab moves us back to
            STATE_NOT_COMPLETING.

        When we transition state we obviously also need to reset our state
        variables appropriately.

        :param: buffer_content the current buffer contents, should be path-like
        """
        if self.state == STATE_NOT_COMPLETING:
            if buffer_content.endswith('\t'):
                self.state = STATE_COMPLETING
                self.completion_base = buffer_content.replace("\t", "")
                self.previous_completion = None
                # sublime.message_dialog("Entering COMPLETING, base: {0}".format(self.completion_base))
        elif self.state == STATE_COMPLETING:
            if not buffer_content.endswith('\t'):
                self.state = STATE_NOT_COMPLETING
                self.completion_base = None
                self.previous_completion = None
                # sublime.message_dialog("Entering NOT_COMPLETING")

    def complete(self, buffer_content):
        """Return a completion, or None if we're not in STATE_COMPLETING.

        This method implements a simple looping buffer approach to completions.
        For each press of the tab key, the method will return the next
        available completion from the base that was set when transitioning
        into STATE_COMPLETING.

        :param: buffer_content the current buffer contents, should be path-like.
                    Required so we can return it if there is no completion.
        """
        if not self.state == STATE_COMPLETING:
            return None

        current_path = self.completion_base

        # If we have ~, we need to expand and add the slash, otherwise
        # just expand what we have and leave it for completion.
        if current_path == '~':
            current_path = os.path.expanduser(current_path) + os.sep
        elif current_path.startswith('~'):
            current_path = os.path.expanduser(current_path)

        # Now do a simple match to find the first prefix matched subfolder
        directory, fname = os.path.split(current_path)
        subfolders = [o for o in os.listdir(directory) if os.path.isdir(os.path.join(directory, o))]

        # Now find the possible candidates. Getting all and putting in a list
        # allows us to loop through them using the previous_completion state
        # variable.
        candidates = []
        search_prefix = fname.lower()
        for f in subfolders:
            candidate = f.lower()
            if candidate.startswith(search_prefix):
                candidates.append(f)

        if not candidates:
            # At minimum, return the existing content minus the tab
            return buffer_content.replace("\t", "")

        # stabilise the ordering
        candidates = sorted(candidates)

        if not self.previous_completion:  # Return the first
            result = candidates[0]
        else:  # figure the next candidate or loop around
            next_completion_idx = candidates.index(self.previous_completion) + 1
            if next_completion_idx >= len(candidates):
                result = candidates[0]
            else:
                result = candidates[next_completion_idx]

        self.previous_completion = result
        return os.path.join(directory, result) + os.sep

