class Meeting:
    def __init__(self, meeting_id, title, start_time, end_time, attendees):
        self.meeting_id = meeting_id
        self.title = title
        self.start_time = start_time  # Expecting datetime objects
        self.end_time = end_time        # Expecting datetime objects
        self.attendees = attendees      # List of attendee emails

    def __str__(self):
        return f'Meeting({self.title}, {self.start_time}, {self.end_time}, {self.attendees})'


class MeetingManager:
    def __init__(self):
        self.meetings = []  # List to store Meeting objects

    def create_meeting(self, meeting):
        if self.check_overlap(meeting):
            raise ValueError('Meeting time overlaps with an existing meeting.')
        self.meetings.append(meeting)

    def update_meeting(self, updated_meeting):
        for i, meeting in enumerate(self.meetings):
            if meeting.meeting_id == updated_meeting.meeting_id:
                if self.check_overlap(updated_meeting, skip_index=i):
                    raise ValueError('Meeting time overlaps with an existing meeting.')
                self.meetings[i] = updated_meeting
                return
        raise ValueError('Meeting not found.')

    def delete_meeting(self, meeting_id):
        for i, meeting in enumerate(self.meetings):
            if meeting.meeting_id == meeting_id:
                self.meetings.pop(i)
                return
        raise ValueError('Meeting not found.')

    def get_meetings(self):
        return self.meetings

    def check_overlap(self, new_meeting, skip_index=None):
        for i, existing_meeting in enumerate(self.meetings):
            if skip_index is not None and i == skip_index:
                continue  # Skip the meeting being updated
            if (new_meeting.start_time < existing_meeting.end_time and
                    new_meeting.end_time > existing_meeting.start_time):
                return True  # Overlapping meeting found
        return False  # No overlap
