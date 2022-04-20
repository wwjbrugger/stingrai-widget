
class TransitionToUseController():
    def __init__(self, num_of_transition, fraction_change_transition):
        try:
            self.fraction_change_transition = fraction_change_transition
        except AttributeError:
            self.fraction_change_transition = 0
        self.change_position = max(0, int(num_of_transition * self.fraction_change_transition) - 1)
        self.flag_change_done = False
        self.files_processed = 0


    def choose_transition_to_use(self, transition):
        transition_to_use = transition
        if transition == 'background->signal':
            if self.files_processed < self.change_position:
                # before change
                transition_to_use = 'background->background'
            elif self.files_processed >= self.change_position and not self.flag_change_done:
                # handles change
                transition_to_use = 'background->signal'
                self.flag_change_done = True
            else:
                # after change
                transition_to_use = 'signal->signal'

        if transition == 'signal->background':
            if self.files_processed < self.change_position:
                # before change
                transition_to_use = 'signal->signal'
            elif self.files_processed >= self.change_position and not self.flag_change_done:
                # handles change
                transition_to_use = 'signal->background'
                self.flag_change_done = True
            else:
                # after change
                transition_to_use = 'background->background'
        self.files_processed += 1
        return transition_to_use