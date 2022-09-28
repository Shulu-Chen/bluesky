

class eVTOL:
    '''
    Creating class of type eVTOL
    '''
    def __init__(self,sequence_number, ETA, cruise_speed, max_speed, buffer = 3600):
        self.ETA = ETA
        self.RTA = ETA
        self.original_sequence_number = sequence_number
        self.vertiport_landing_number = sequence_number
        self.earliest_ETA = ETA * cruise_speed / max_speed
        self.latest_ETA = ETA + buffer
        # Buffer between 10 to 15 minutes randomly chosen for battery reserve
